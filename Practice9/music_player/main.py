import pygame
import sys
from player import MusicPlayer

# Window settings
WIDTH, HEIGHT = 600, 450
FPS = 30
TITLE = "🎵 Music Player"

# Colors
BG_COLOR       = (15, 15, 30)
PANEL_COLOR    = (30, 30, 55)
ACCENT_COLOR   = (100, 200, 255)
WHITE          = (255, 255, 255)
GRAY           = (150, 150, 170)
GREEN          = (80, 220, 120)
RED            = (255, 80, 80)
YELLOW         = (255, 220, 60)


def draw_ui(screen, player, fonts):
    font_title, font_main, font_small, font_key = fonts
    screen.fill(BG_COLOR)

    # Title bar
    pygame.draw.rect(screen, PANEL_COLOR, (0, 0, WIDTH, 70))
    title_surf = font_title.render("🎵  Music Player", True, ACCENT_COLOR)
    screen.blit(title_surf, (20, 18))

    # Track info panel
    pygame.draw.rect(screen, PANEL_COLOR, (20, 90, WIDTH - 40, 90), border_radius=12)

    # Status
    status_color = GREEN if "Playing" in player.get_status() else RED
    status_surf = font_main.render(player.get_status(), True, status_color)
    screen.blit(status_surf, (40, 105))

    # Track name
    track_name = player.get_current_name()
    if len(track_name) > 35:
        track_name = track_name[:32] + "..."
    track_surf = font_main.render(f"♪  {track_name}", True, WHITE)
    screen.blit(track_surf, (40, 140))

    # Track counter
    if player.playlist:
        counter = f"Track {player.current_index + 1} / {len(player.playlist)}"
    else:
        counter = "No tracks loaded"
    counter_surf = font_small.render(counter, True, GRAY)
    screen.blit(counter_surf, (40, 168))

    # Volume bar
    pygame.draw.rect(screen, PANEL_COLOR, (20, 200, WIDTH - 40, 55), border_radius=12)
    vol_label = font_small.render("Volume:", True, GRAY)
    screen.blit(vol_label, (40, 215))

    bar_x, bar_y, bar_w, bar_h = 130, 218, 340, 20
    pygame.draw.rect(screen, (50, 50, 80), (bar_x, bar_y, bar_w, bar_h), border_radius=8)
    fill_w = int(bar_w * player.volume)
    pygame.draw.rect(screen, ACCENT_COLOR, (bar_x, bar_y, fill_w, bar_h), border_radius=8)
    vol_pct = font_small.render(f"{int(player.volume * 100)}%", True, WHITE)
    screen.blit(vol_pct, (480, 215))

    # Keyboard controls reference
    pygame.draw.rect(screen, PANEL_COLOR, (20, 275, WIDTH - 40, 150), border_radius=12)
    controls_title = font_small.render("Keyboard Controls", True, ACCENT_COLOR)
    screen.blit(controls_title, (40, 288))

    controls = [
        ("[P]", "Play"),
        ("[S]", "Stop"),
        ("[N]", "Next track"),
        ("[B]", "Previous track"),
        ("[↑] [↓]", "Volume up / down"),
        ("[Q] / [ESC]", "Quit"),
    ]

    col1_x, col2_x = 40, 150
    row_y = 315
    for i, (key, desc) in enumerate(controls):
        col = i % 2
        row = i // 2
        x = col1_x if col == 0 else WIDTH // 2
        y = row_y + row * 28
        key_surf = font_key.render(key, True, YELLOW)
        desc_surf = font_small.render(desc, True, WHITE)
        screen.blit(key_surf, (x, y))
        screen.blit(desc_surf, (x + 90, y))

    # Playlist (if tracks loaded)
    if not player.playlist:
        hint = font_small.render("Put audio files in the 'music/' folder and restart.", True, GRAY)
        screen.blit(hint, (40, 440))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    # Fonts
    font_title = pygame.font.SysFont("Arial", 26, bold=True)
    font_main  = pygame.font.SysFont("Arial", 22)
    font_small = pygame.font.SysFont("Arial", 18)
    font_key   = pygame.font.SysFont("Courier", 18, bold=True)
    fonts = (font_title, font_main, font_small, font_key)

    # Create player and load music
    player = MusicPlayer()
    player.load_playlist("music")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    player.play()
                elif event.key == pygame.K_s:
                    player.stop()
                elif event.key == pygame.K_n:
                    player.next_track()
                elif event.key == pygame.K_b:
                    player.prev_track()
                elif event.key == pygame.K_UP:
                    player.volume_up()
                elif event.key == pygame.K_DOWN:
                    player.volume_down()
                elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                    running = False

        # Auto-advance to next track when current ends
        player.check_auto_next()

        draw_ui(screen, player, fonts)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
