# Music Player 🎵

An interactive music player with keyboard controls built with Pygame.

## Features
- Play, Stop, Next, Previous track controls
- Volume control
- Displays current track name and status
- Auto-advances to next track when current ends
- Supports MP3, WAV, OGG, FLAC formats

## How to Run
```bash
pip install pygame
# Place audio files in the music/ folder
python main.py
```

## Keyboard Controls
| Key       | Action         |
|-----------|----------------|
| `P`       | Play           |
| `S`       | Stop           |
| `N`       | Next track     |
| `B`       | Previous track |
| `↑`       | Volume up      |
| `↓`       | Volume down    |
| `Q`/`ESC` | Quit           |

## Files
- `main.py` — Entry point, game loop, UI rendering
- `player.py` — MusicPlayer class with playlist logic
- `music/` — Place your audio files here
