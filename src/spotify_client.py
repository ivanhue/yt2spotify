import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
from typing import List, Optional
import logging

from src.entities import Song
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI

class SpotifyClientError(Exception):
    """Custom exception for Spotify client errors."""
    pass

class SpotifyClient:
    """
    Client to interact with Spotify API.
    
    This class allows search songs and create playlists using spotipy library.
    """
    def __init__(self, client_id: str = SPOTIFY_CLIENT_ID, client_secret: str = SPOTIFY_CLIENT_SECRET, redirect_uri: str = SPOTIPY_REDIRECT_URI):
        """
        Initialize the Spotify client.
        
        Args:
            client
        """
        self.logger = logging.getLogger(__name__)
        scope = "playlist-modify-public playlist-modify-private"
        
        auth_manager_kwargs = {"scope": scope}
        if client_id:
            auth_manager_kwargs["client_id"] = client_id
        if client_secret:
            auth_manager_kwargs["client_secret"] = client_secret
        if redirect_uri:
            auth_manager_kwargs["redirect_uri"] = redirect_uri

        try:
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(**auth_manager_kwargs))
            # Verify authentication
            self.sp.current_user()
        except SpotifyException as e:
            raise SpotifyClientError(f"Failed initializing Spotify client: {str(e)}")
            

    def search_track(self, song: Song) -> str | None:
        """
        Search a song in Spotify and return its ID.
        
        Args:
            song: Song object with information about the song
        
        Returns:
            Song ID from Spotify or None if it is not found
        """
        try:
            query = song.title
            if hasattr(song, "artist") and song.artist:
                query = f"{song.title} artist:{song.artist}"
                
            song_result = self.sp.search(q=query, type='track', limit=1)
            items = song_result.get("tracks", {}).get("items", [])
            
            if items:
                track_id = items[0]["id"]
                return track_id
            else:
                self.logger.warning(f"Song not found: {song.title}")
                return None
        
        except SpotifyException as e:
            raise SpotifyClientError(f"Error searching the song '{song.title}': {str(e)}")
        

    def create_playlist(self, name: str, description: str, track_ids: List[str]) -> str:
        """
        Create a playlist in Spotify from a list of songs.
        
        Args:
            name: Playlist name
            description: Playlist description
            track_ids: Song IDs list from Spotify
        
        Returns:
            Playlist URL created
        
        Raises:
            SpotifyClientException: If there is an error creating playlist
            ValueError: If there is not valid songs provided 
        """
        if not track_ids:
            raise ValueError("Could not create playlists empty")
        
        # Filter valid IDs
        valid_track_ids = [track_id for track_id in track_ids if track_id is not None]
        
        if not valid_track_ids:
            raise ValueError("There are not songs valid to create playlist")
        
        try:
            user_id = self.sp.current_user()["id"]
            
            playlist = self.sp.user_playlist_create(
                user=user_id,
                name=name,
                public=False,
                description=description
            )
            
            # Spotify has a limit of 100 songs per request
            batch_size = 100
            for i in range(0, len(valid_track_ids), batch_size):
                batch = valid_track_ids[i:i+batch_size]
                self.sp.playlist_add_items(playlist["id"], batch)
                
            self.logger.info(f"Playlist '{name}' created succesfully with {len(valid_track_ids)} songs")
            return playlist["external_urls"]["spotify"]
        
        except SpotifyException as e:
            raise SpotifyClientError(f"Error creating the playlist '{name}': {str(e)}")
        
    
    def get_user_info(self) -> dict:
        """
        Get information from current user.
        
        Returns:
            A dict with user information
        """
        try:
            return self.sp.current_user()
        except SpotifyException as e:
            raise SpotifyClientError(f"Error obtaining user information: {str(e)}")