# 🎵 YouTube to Spotify Playlist Converter

This project allows you to convert a YouTube Music playlist into a Spotify playlist automatically, using the command line.

It was created to practice working with APIs, Python scripting, and playlist management between two major music platforms.

## 🚀 Features

- Convert public playlists from YouTube Music to Spotify
- Create new playlists in your Spotify account
- Automatically search and match songs
- Show progress and summary of the conversion
- Command-line interface with helpful messages and validation

## 🛠 Technologies Used

- Python 3.10+
- [Click](https://click.palletsprojects.com/) for command-line interface
- [ytmusicapi](https://ytmusicapi.readthedocs.io/en/latest/) to get YouTube Music data
- [Spotipy](https://spotipy.readthedocs.io/en/2.22.1/) to interact with the Spotify API
- Logging module for debugging and detailed information

## 📦 Installation

1. Clone the repository:

```bash
git clone https://github.com/ivanhue/yt2spotify.git
cd yt2spotify
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Set up your environment variables:

```env
# YouTube credentials
YOUTUBE_CLIENT_ID=your_youtube_client_id
YOUTUBE_CLIENT_SECRET=your_youtube_client_secret

# Spotify credentials
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
```

🔐 **OAuth Authentication**

As of November 2024, YouTube Music requires a Client ID and Client Secret for the YouTube Data API. To obtain them:

1. Go to the [YouTube Data API documentation](https://developers.google.com/youtube/registering_an_application)
2. Use your Google Cloud Console account and create a project
3. Enable the YouTube Data API and generate OAuth credentials

Spotify also requires OAuth authentication to authorize your account and generate tokens. You can set these up through the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).

## ▶️ Usage

Run the tool from the command line:

```bash
python main.py "https://music.youtube.com/playlist?list=YOUR_PLAYLIST_ID"
```

### Optional parameters:

- `--name` or `-n`: Set a custom name for the new Spotify playlist
- `--description` or `-d`: Add a description to the Spotify playlist
- `--verbose` or `-v`: Show detailed information during the process

### Example:

```bash
python main.py "https://music.youtube.com/playlist?list=PL123ABC" --name "My Converted Playlist" --verbose
```

## 📊 Output

After the conversion, you will see a summary with:

- Total songs found
- Number of songs added to Spotify
- Number of songs not found
- Success rate (%)

## 🧪 Limitations

- Functionality may change depending on updates in external libraries or APIs
- YouTube Music may update the way credentials are obtained in the future
- Song matching between platforms is not always 100% accurate and may result in missing songs

## 📄 License

This project is open source and free to use for educational purposes.

## 🙋 About Me

This project was developed by **Alejandro Ivan** as a portfolio project to demonstrate skills in Python, API integration, and command-line tools.

Feel free to contact me or check out more of my work!