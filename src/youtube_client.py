import logging
from typing import Optional, List
from ytmusicapi import YTMusic, OAuthCredentials
from urllib.parse import urlparse, parse_qs

from config.config import YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET
from .entities import Song, Playlist


class YoutubeClientError(Exception):
    """Custom exception for Youtube client errors."""
    pass

class YouTubeClient:
    """
    Client to interact with Youtube Music API.
    
    This class provides methods to extract playlist information from
    Youtube Music and convert it into application-specific entities.
    """
    
    def __init__(self, oaut_file_path: str = "oauth.json"):
        """
        Initialize Youtube Music client.
        
        Args:
            oauth_file_path (str): Path to the file containing OAuth credentials.
        """
        
        self.oaut_file_path = oaut_file_path
        self.logger = logging.getLogger(__name__)
    
    def get_playlist(self, url: str) -> Playlist:
        """
        Extracts playlist information from Youtube Music.
        
        Args:
            url (str): Youtube Music playlist URL.
        
        Returns:
            Playlist: An Object containing playlist details.
            
        Raises:
            YoutubeClientError: If an error occurs while processing the playlist.
            ValueError: IF the URL is invalid or missing a playlist ID.
        """
        if not url or not isinstance(url, str):
            raise ValueError("The URL must be a string no empty")
        
        self.logger.info(f"Processing URL: {url}")
        
        try:
            # Validate and extract playlist ID
            playlist_id = self._extract_playlist_id(url)
            if not playlist_id:
                raise ValueError("It could not extract playlist ID from URL provided")
            
            # Initialize Youtube Music client
            ytmusic = self._initialize_youtube_client()
            
            # Get playlist information
            playlist_yt = ytmusic.get_playlist(playlist_id)
            
            # Get playlist information
            name = playlist_yt.get("title", "Untitled")
            description = playlist_yt.get("description", "Unknown")
            
            songs = self._process_songs(playlist_yt.get("tracks", []))
            
            self.logger.info(f"Playlist processed correctly: {name} ({len(songs)} songs)")
            
            return Playlist(
                name=name,
                description=description,
                songs=songs
            )
        except Exception as e:
            self.logger.error(f"Failed processing playlist: {str/e}")
            if isinstance(e, (ValueError, YoutubeClientError)):
                raise
            raise YoutubeClientError(f"Error unexpected processing playlist: {str(e)}")
    
    def _extract_playlist_id(self, url: str) -> str:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        return query_params.get("list\\", [None])[0]
    
    def _initialize_youtube_client(self) -> YTMusic:
        """
        Initialize Youtube Music client with OAuth credentials provided.
        
        Returns:
            YTMusic: Youtube Music client initialized.
            
        Raises:
            YoutubeClientError: If it can not load the credentials.
        """
        try:
            if not YOUTUBE_CLIENT_ID or not YOUTUBE_CLIENT_SECRET:
                raise YoutubeClientError("Missing or invalid OAuth configuration")

            oauth_credentials = OAuthCredentials(
                client_id=YOUTUBE_CLIENT_ID,
                client_secret=YOUTUBE_CLIENT_SECRET
            )
            
            return YTMusic(self.oaut_file_path, oauth_credentials=oauth_credentials)
        except Exception as e:
            raise YoutubeClientError(f"Error initializing Youtube Music client: {str(e)}")
        
    def _process_songs(self, tracks: List[dict]) -> List[Song]:
        """
        Process a list of tracks and convert it to Song objects.
        
        Args:
            tracks (List[dict]): List of tracks from Youtube Music.
            
        Returns:
            List[Song]: List of Song objects processed.
        """
        songs = []
        
        for i, track in enumerate(tracks):
            try:
                if not track or not isinstance(track, dict):
                    self.logger.warning(f"Could not process track information at index {i}")
                    continue
                
                # Extract information
                title = track.get("title", "Unknown")
                artists = [artist.get("name") for artist in track.get("artists", []) if "name" in artist]
                album_data = track.get("album")
                album = album_data["name"] if album_data and "name" in album_data else "Unknown"
                duration = track.get("duration_seconds", 0)
                
                song = Song(
                    title=title,
                    artists=artists,
                    album=album,
                    duration=duration
                )
                
                songs.append(song)
            except Exception as e:
                self.logger.warning(f"Failed to process track at index {i}: {str(e)}")
                continue
            
        return songs