# Moving Ball Game 🔴

An interactive game with a moving red ball built with Pygame.

## Features
- Red ball (radius 25, 50×50 pixels) on white background
- Move with arrow keys
- 20 pixels per key press
- Ball cannot leave screen boundaries (invalid moves are ignored)
- Visual grid and position display

## How to Run
```bash
pip install pygame
python main.py
```

## Controls
| Key         | Action              |
|-------------|---------------------|
| `↑ ↓ ← →`  | Move ball           |
| `R`         | Reset to center     |
| `Q`/`ESC`   | Quit                |

## Files
- `main.py` — Entry point, game loop, rendering
- `ball.py` — Ball class with movement and boundary logic