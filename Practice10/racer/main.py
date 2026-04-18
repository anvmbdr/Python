import pygame
import sys
import random
from car import PlayerCar, EnemyCar
from coin import Coin

# ── Window & game constants ─────────────────────────────────────────────────
WIDTH, HEIGHT = 400, 600
FPS = 60
TITLE = "Racer"

# Road lane boundaries (x positions where cars can drive)
LANE_POSITIONS = [80, 160, 240, 320]

# Colors
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0  )
YELLOW = (255, 215, 0  )
GRAY   = (80,  80,  80 )
GREEN  = (34, 139,  34 )
RED    = (220,  40,  40 )


def draw_road(screen, offset):
    # Green sides
    pygame.draw.rect(screen, GREEN, (0, 0, 60, HEIGHT))
    pygame.draw.rect(screen, GREEN, (340, 0, 60, HEIGHT))

    # Road surface
    pygame.draw.rect(screen, GRAY, (60, 0, 280, HEIGHT))

    # White edge lines
    pygame.draw.rect(screen, WHITE, (60,  0, 5, HEIGHT))
    pygame.draw.rect(screen, WHITE, (335, 0, 5, HEIGHT))

    # Dashed centre dividers (scrolling)
    for lane_x in [130, 200, 270]:
        for y in range(-60, HEIGHT + 60, 60):
            y_pos = (y + offset) % (HEIGHT + 60) - 60
            pygame.draw.rect(screen, WHITE, (lane_x, y_pos, 5, 40))


def draw_hud(screen, score, coins, font_big, font_small):
    # Score
    score_surf = font_big.render(f"Score: {score}", True, WHITE)
    screen.blit(score_surf, (10, 10))

    # Coin count — top right corner (extra task)
    coin_surf = font_big.render(f"Coins: {coins}", True, YELLOW)
    screen.blit(coin_surf, (WIDTH - coin_surf.get_width() - 10, 10))


def draw_game_over(screen, score, coins, font_big, font_small):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))

    over_surf  = font_big.render("GAME OVER", True, RED)
    score_surf = font_small.render(f"Score: {score}  |  Coins: {coins}", True, WHITE)
    retry_surf = font_small.render("Press R to restart  or  Q to quit", True, (200, 200, 200))

    screen.blit(over_surf,  over_surf.get_rect(center=(WIDTH//2, HEIGHT//2 - 50)))
    screen.blit(score_surf, score_surf.get_rect(center=(WIDTH//2, HEIGHT//2 + 10)))
    screen.blit(retry_surf, retry_surf.get_rect(center=(WIDTH//2, HEIGHT//2 + 55)))


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    font_big   = pygame.font.SysFont("Arial", 26, bold=True)
    font_small = pygame.font.SysFont("Arial", 20)

    # ── Game state ──────────────────────────────────────────────────────────
    player     = PlayerCar(WIDTH // 2 - 25, HEIGHT - 120)
    enemies    = []          # List of active enemy cars
    coins      = []          # List of active coins (extra task)
    road_offset = 0          # Used for scrolling road animation
    score      = 0
    coin_count = 0           # Collected coins counter (extra task)
    speed      = 5           # Starting scroll speed
    game_over  = False

    # Timers for spawning enemies and coins
    enemy_timer = 0
    coin_timer  = 0

    running = True
    while running:
        dt = clock.tick(FPS)  # Delta time in milliseconds

        # ── Events ──────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if game_over and event.key == pygame.K_r:
                    return  # Restart by re-calling run_game()

        # ── Input handling ──────────────────────────────────────────────────
        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.move_left()
            if keys[pygame.K_RIGHT]:
                player.move_right()
            if keys[pygame.K_UP]:
                player.move_up()
            if keys[pygame.K_DOWN]:
                player.move_down()

            # Keep player within road boundaries
            player.clamp(60, 335)

        # ── Update ──────────────────────────────────────────────────────────
        if not game_over:
            # Scroll road downward
            road_offset = (road_offset + speed) % 60

            # Gradually increase speed over time (increases difficulty)
            score += 1
            if score % 500 == 0:
                speed = min(speed + 1, 20)

            # Spawn enemy car every ~90 frames
            enemy_timer += 1
            if enemy_timer >= 90:
                enemy_timer = 0
                lane_x = random.choice(LANE_POSITIONS) - 25
                enemies.append(EnemyCar(lane_x, -90))

            # Spawn coin randomly on road (extra task)
            coin_timer += 1
            if coin_timer >= 120:
                coin_timer = random.randint(0, 30)  # randomize next spawn
                lane_x = random.choice(LANE_POSITIONS) - 15
                coins.append(Coin(lane_x, -40))

            # Move enemies downward and remove off-screen ones
            for enemy in enemies[:]:
                enemy.update(speed)
                if enemy.rect.top > HEIGHT:
                    enemies.remove(enemy)

            # Move coins downward (extra task)
            for coin in coins[:]:
                coin.update(speed)
                if coin.rect.top > HEIGHT:
                    coins.remove(coin)

            # Check player ↔ enemy collision → game over
            for enemy in enemies:
                if player.rect.colliderect(enemy.rect):
                    game_over = True

            # Check player ↔ coin collision → collect coin (extra task)
            for coin in coins[:]:
                if player.rect.colliderect(coin.rect):
                    coins.remove(coin)
                    coin_count += 1  # Increment coin counter

        # ── Draw ────────────────────────────────────────────────────────────
        draw_road(screen, road_offset)

        for coin in coins:
            coin.draw(screen)       # Draw coins under cars

        player.draw(screen)

        for enemy in enemies:
            enemy.draw(screen)

        draw_hud(screen, score // 10, coin_count, font_big, font_small)

        if game_over:
            draw_game_over(screen, score // 10, coin_count, font_big, font_small)

        pygame.display.flip()

    pygame.quit()


# ── Entry point ──────────────────────────────────────────────────────────────
while True:
    run_game()
