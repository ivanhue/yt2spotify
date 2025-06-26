# src/entities.py
from dataclasses import dataclass
from typing import List

@dataclass
class Song:
    title: str
    artists: List[str]
    album: str
    duration: int  # seconds

@dataclass
class Playlist:
    name: str
    description: str
    songs: List[Song]