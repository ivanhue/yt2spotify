"""
YouTube to Spotify Playlist Converter

Converts playlist from Youtube to Spotify automatically.
"""
import sys
import logging
from typing import Optional
import click

from src import YouTubeClient, SpotifyClient, PlaylistConverter, PlaylistConverterError

def setup_logging(verbose: bool = False) -> None:
    """Configure logging system."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

@click.command()
@click.argument("youtube_url", required=True)
@click.option(
    "--name", "-n",
    help="Custom name for playlist"
)
@click.option(
    "--description", "-d", 
    help="Custom description for playlist"
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="Show detailed process information"
)
def main(
        youtube_url: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        verbose: bool = False
    ) -> None:
    """
    Converts a playlist from Youtube to Spotify.
    
    YOUTUBE_URL: Youtube playlist URL to convert
    
    Example:
        python main.py "https://music.youtube.com/playlist\?list\=P.."
    """
    setup_logging(verbose)
    logger = logging.getLogger(__name__)
    
    try:
        if not youtube_url.startswith('https://'):
            raise click.BadParameter("The URL must start with https://")
        
        if 'youtube.com' not in youtube_url and 'youtube.be' not in youtube_url:
            raise click.BadParameter("The URL must be from Youtube")
        
        click.echo("🎵 YouTube to Spotify Playlist Converter")
        click.echo("=" * 40)
        
        # Initializing clientes
        click.echo("Initializing clients...")
    
        try:    
            yt_client = YouTubeClient()
            spotify_client = SpotifyClient()
            converter = PlaylistConverter(yt_client, spotify_client)
        except Exception as e:
            logger.error(f"Failed initializing clients: {e}")
            click.echo(f"Failed to initialize: {e}", err=True)
            sys.exit(1)
            
        with click.progressbar(length=100, label="Converting playlist") as bar:
            try:
                result = converter.convert(
                    youtube_url=youtube_url,
                    playlist_name=name,
                    playlist_description=description
                )
                bar.update(100)
            except PlaylistConverterError as e:
                click.echo(f"\nError during conversion: {e}", err=True)
                sys.exit(1)
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                click.error(f"\nUnexpected error: {e}", err=True)
                sys.exit(1)
                
        # Show results
        click.echo("\n✅ Conversion completed!")
        click.echo("=" * 40)
        click.echo("📊 Detailed summary:")
        summary = converter.get_conversion_summary(result)
        click.echo(summary)
    
    except click.BadParameter as e:
        click.echo(f"Invalid parameter: {e}", err=True)
        sys.exit(1)
    except KeyboardInterrupt:
        click.echo("\nProcess interrupted by user", err=True)
        sys.exit(1)
    except Exception as e:
        logger.error(f"Critical error: {e}")
        click.echo(f"Critical error: {e}", err=True)
        sys.exit(1)
    
if __name__ == '__main__':
    main()