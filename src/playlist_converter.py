from typing import List, Tuple, Optional
import logging
from dataclasses import dataclass

from src import YouTubeClient, SpotifyClient
from .entities import Song

@dataclass
class ConversionResult:
    """Result of a playlist conversion."""
    playlist_url: str
    failed_songs: List[Song]
    total_songs: int
    converted_songs: int
    
    @property
    def success_rate(self) -> float:
        """Calculate the percentage of successful conversionts."""
        if self.total_songs == 0:
            return 0.0
        return (self.total_songs / self.converted_songs) * 100
    
class PlaylistConverterError(Exception):
    """Custom exception for playlist conversion."""
    pass


class PlaylistConverter:
    """
    Convert YouTube playlists to Spotify.
    
    This class allows you to extract songs from a Youtube playlist and
    create am equivalent playlist on Spotify.
    """
    def __init__(self, yt_client: YouTubeClient, spotify_client: SpotifyClient):
        """
        Initialize the playlist converter.
        
        Args:
            yt_client: YouTube client to extract playlists
            spotify_client: Spotify client to create playlists
        """
        self.yt = yt_client
        self.spotify = spotify_client
        self.logger = logging.getLogger(__name__)

    def convert(self, youtube_url: str, playlist_name: Optional[str] = None,
                playlist_description: Optional[str] = None) -> ConversionResult:
        """
        Convert a YouTube playlist to Spotify.
        
        Args:
            youtube_url: Youtube playlist URL
            playlist_name: Custom playlist name (optional)
            playlist_description: Custom description (optional)
        
        Returns:
            ConversionResult with detailed information about conversion
            
        Raises:
            PlaylistConverterError: If there is an error during conversion
            ValueError: If URL is invalid
        """
        if not youtube_url or not isinstance(youtube_url, str):
            raise ValueError("Youtube URL must be a non-empty string")
        
        try:
            self.logger.info(f"Obtaining YouTube playlist: {youtube_url}")
            playlist = self.yt.get_playlist(youtube_url)
            
            if not playlist.songs:
                raise PlaylistConverterError("Youtube playlist is empty")
            
            self.logger.info(f"Found {len(playlist.songs)} songs in playlist")
            
            # Converting songs
            spotify_ids, failed_songs = self._convert_songs(playlist.songs)
            
            if not spotify_ids:
                raise PlaylistConverterError("Could not find any song on Spotify")
            
            final_name = playlist_name or playlist.name or "Playlist from Youtube"
            final_description = (playlist_description or 
                                 playlist.description or 
                                 f"Playlist converted from Youtube. {len(failed_songs)} songs not found.")
            
            self.logger.info(f"Creating Spotify playlist '{final_name}'")
            playlist_url = self.spotify.create_playlist(
                name=final_name,
                description=final_description,
                track_ids=spotify_ids
            )
            
            result = ConversionResult(
                playlist_url=playlist_url,
                failed_songs=failed_songs,
                total_songs=len(playlist.songs),
                converted_songs=len(spotify_ids)
            )
            
            self.logger.info(
                f"Conversion completed. {result.converted_songs}/{result.total_songs} "
                f"songs converted ({result.success_rate:.1f}%)"
            )
            
            return result
        
        except Exception as e:
            self.logger.error(f"Error during conversion: {e}")
            if isinstance(e, (PlaylistConverterError, ValueError)):
                raise
            raise PlaylistConverterError(f"Unexpected error during conversion: {str(e)}") from e
        
    def _convert_songs(self, songs: List[Song]) -> Tuple[List[str], List[Song]]:
        """
        Convert a list of YouTube songs into Spotify track IDs.
        
        Args:
            songs: Songs list from Youtube
            
        Returns:
            Tuple of Spotify IDs found and songs not found
        """
        spotify_ids = []
        failed_songs = []
        for i, song in enumerate(songs, 1):
            self.logger.debug(f"Processing song {i}/{len(songs)}: {song.title}")
            
            try:
                track_id = self.spotify.search_track(song)
                if track_id:
                    spotify_ids.append(track_id)
                    self.logger.debug(f"✅ Found: {song.title}")
                else:
                    failed_songs.append(song)
                    self.logger.warning(f"❌ Not found: {song.title}")
            except Exception as e:
                self.logger.error(f"Error searching {song.title}: {e}")
                failed_songs.append(song)
    
        return spotify_ids, failed_songs
    
    def get_conversion_summary(self, result: ConversionResult) -> str:
        """
        Generate a readable summary of the conversion.
        
        Args:
            result: Conversion result
            
        Returns:
            String with summary of the conversion
        """
        summary = f"""
        Conversion of playlist completed:
        - Playlist created: {result.playlist_url}
        - Total songs: {result.total_songs}
        - Songs converted: {result.converted_songs}
        - Songs not found: {len(result.failed_songs)}
        - Success rate: {result.success_rate:.1f}%
        """
        
        if result.failed_songs:
            summary += "\nSongs not found:\n"
            for song in result.failed_songs:
                summary += f"- {song.title}\n"
        
        return summary.strip()
        