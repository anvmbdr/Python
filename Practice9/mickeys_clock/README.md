# Mickey's Clock 🕐

A real-time clock application using Mickey Mouse hand graphics built with Pygame.

## Features
- Displays current system time (hours, minutes, seconds)
- Mickey Mouse hands as clock hands:
  - **Right hand** = Minutes
  - **Left hand** = Seconds
- Real-time synchronization with system clock
- Digital time display
- Decorative clock face with markers

## How to Run
```bash
pip install pygame
python main.py
```

## Controls
- `Q` or `ESC` — Quit

## Files
- `main.py` — Entry point, game loop
- `clock.py` — MickeysClock class with drawing logic
- `images/mickey_hand.png` — Mickey hand graphic (optional; auto-generated if missing)
