import pygame
import sys
import random
from car import PlayerCar, EnemyCar
from coin import Coin, random_coin_type

# ── Window & game settings ───────────────────────────────────────────────────
WIDTH, HEIGHT = 400, 600
FPS           = 60
TITLE         = "Racer — Practice 11"

# X positions of the four driveable lanes (car center)
LANE_POSITIONS = [80, 160, 240, 320]

# How many coins the player must collect before enemies get faster
SPEED_UP_EVERY = 5      # Every 5 coins → enemy speed +1

# Colors
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0  )
YELLOW = (255, 215, 0  )
GRAY   = (80,  80,  80 )
GREEN  = (34,  139, 34 )
RED    = (220, 40,  40 )
BRONZE = (180, 100, 30 )
SILVER = (180, 180, 190)
GOLD   = (255, 200, 0  )

# Map coin type to HUD color for visual feedback
COIN_COLORS = {"bronze": BRONZE, "silver": SILVER, "gold": GOLD}


def draw_road(screen, offset):
   
    # Green verges on each side
    pygame.draw.rect(screen, GREEN, (0, 0, 60, HEIGHT))
    pygame.draw.rect(screen, GREEN, (340, 0, 60, HEIGHT))

    # Gray tarmac
    pygame.draw.rect(screen, GRAY, (60, 0, 280, HEIGHT))

    # Solid white edge lines
    pygame.draw.rect(screen, WHITE, (60,  0, 5, HEIGHT))
    pygame.draw.rect(screen, WHITE, (335, 0, 5, HEIGHT))

    # Dashed white lane dividers — scrolling downward
    for lane_x in [130, 200, 270]:
        for y in range(-60, HEIGHT + 60, 60):
            y_pos = (y + offset) % (HEIGHT + 60) - 60
            pygame.draw.rect(screen, WHITE, (lane_x, y_pos, 5, 40))


def draw_hud(screen, score, coin_total, enemy_speed, next_speedup, font):

    # Score
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))

    # Total coins (top right) — extra task display
    coin_surf = font.render(f"Coins: {coin_total}", True, GOLD)
    screen.blit(coin_surf, (WIDTH - coin_surf.get_width() - 10, 10))

    # Enemy speed indicator
    spd_surf = font.render(f"Enemy spd: {enemy_speed}", True, (255, 120, 120))
    screen.blit(spd_surf, (10, 35))

    # Progress bar: coins until next speed boost
    progress  = (coin_total % SPEED_UP_EVERY) / SPEED_UP_EVERY
    bar_x, bar_y, bar_w, bar_h = 10, 58, 140, 10
    pygame.draw.rect(screen, (80, 80, 80), (bar_x, bar_y, bar_w, bar_h), border_radius=4)
    pygame.draw.rect(screen, (255, 160, 0),
                     (bar_x, bar_y, int(bar_w * progress), bar_h), border_radius=4)
    lbl = font.render(f"+spd in {SPEED_UP_EVERY - coin_total % SPEED_UP_EVERY} coins", True, (200,200,200))
    screen.blit(lbl, (155, 53))


def draw_game_over(screen, score, coins, font_big, font_small):

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))

    screen.blit(font_big.render("GAME OVER", True, RED),
                font_big.render("GAME OVER", True, RED).get_rect(center=(WIDTH//2, HEIGHT//2 - 55)))
    screen.blit(font_small.render(f"Score: {score}   |   Coins: {coins}", True, WHITE),
                font_small.render(f"Score: {score}   |   Coins: {coins}", True, WHITE)
                .get_rect(center=(WIDTH//2, HEIGHT//2 + 5)))
    screen.blit(font_small.render("R — Restart     Q — Quit", True, (200,200,200)),
                font_small.render("R — Restart     Q — Quit", True, (200,200,200))
                .get_rect(center=(WIDTH//2, HEIGHT//2 + 50)))


def run_game():

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock  = pygame.time.Clock()

    font_big   = pygame.font.SysFont("Arial", 28, bold=True)
    font_small = pygame.font.SysFont("Arial", 19)

    # ── Initial state ────────────────────────────────────────────────────────
    player       = PlayerCar(WIDTH // 2 - 25, HEIGHT - 120)
    enemies      = []       # Active enemy cars
    coins        = []       # Active coins on road

    road_offset  = 0        # Scroll animation counter
    road_speed   = 5        # Speed of road + enemy movement
    enemy_speed  = 3        # Enemy cars' own downward speed (separate from road)
    score        = 0        # Increases over time
    coin_total   = 0        # Total coins collected (used for speed threshold)
    game_over    = False

    # Spawn timers
    enemy_timer  = 0
    coin_timer   = 0

    # Flash message when enemy speeds up
    flash_msg    = ""
    flash_timer  = 0

    running = True
    while running:
        clock.tick(FPS)

        # ── Events ──────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit(); sys.exit()
                if game_over and event.key == pygame.K_r:
                    return  # Restart

        # ── Input ────────────────────────────────────────────────────────────
        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:  player.move_left()
            if keys[pygame.K_RIGHT]: player.move_right()
            if keys[pygame.K_UP]:    player.move_up()
            if keys[pygame.K_DOWN]:  player.move_down()
            player.clamp(62, 333)   # Keep player inside road edges

        # ── Update ───────────────────────────────────────────────────────────
        if not game_over:
            # Scroll road
            road_offset = (road_offset + road_speed) % 60
            score += 1
            # Gently increase road scroll speed over time
            if score % 600 == 0:
                road_speed = min(road_speed + 1, 18)

            # ── Spawn enemy every ~90 frames ─────────────────────────────
            enemy_timer += 1
            if enemy_timer >= 90:
                enemy_timer = 0
                lane_x = random.choice(LANE_POSITIONS) - 25
                enemies.append(EnemyCar(lane_x, -90))

            # ── Spawn weighted coin every ~100 frames ────────────────────
            # (task 1: different weights — see coin.py)
            coin_timer += 1
            if coin_timer >= 100:
                coin_timer = random.randint(0, 40)  # randomise next interval
                lane_x = random.choice(LANE_POSITIONS) - 20
                coins.append(Coin(lane_x, -45))     # type chosen inside Coin

            # ── Move enemies ──────────────────────────────────────────────
            for e in enemies[:]:
                e.update(enemy_speed)    # enemy_speed can increase
                if e.rect.top > HEIGHT:
                    enemies.remove(e)

            # ── Move coins ────────────────────────────────────────────────
            for c in coins[:]:
                c.update(road_speed)
                if c.rect.top > HEIGHT:
                    coins.remove(c)

            # ── Collision: player ↔ enemy → game over ─────────────────────
            for e in enemies:
                if player.rect.colliderect(e.rect):
                    game_over = True

            # ── Collision: player ↔ coin → collect ────────────────────────
            for c in coins[:]:
                if player.rect.colliderect(c.rect):
                    coins.remove(c)
                    score      += c.value * 10     # Gold coins give more score
                    coin_total += 1

                    # Task 2: every SPEED_UP_EVERY coins, enemy gets faster
                    if coin_total % SPEED_UP_EVERY == 0:
                        enemy_speed += 1
                        flash_msg   = f"⚡ Enemy faster! Speed {enemy_speed}"
                        flash_timer = 120   # Show for 2 seconds

            # ── Decrement flash timer ─────────────────────────────────────
            if flash_timer > 0:
                flash_timer -= 1

        # ── Draw ─────────────────────────────────────────────────────────────
        draw_road(screen, road_offset)

        for c in coins:    c.draw(screen)
        player.draw(screen)
        for e in enemies:  e.draw(screen)

        draw_hud(screen, score // 10, coin_total, enemy_speed,
                 SPEED_UP_EVERY - coin_total % SPEED_UP_EVERY, font_small)

        # Speed-up flash message
        if flash_timer > 0:
            alpha = min(255, flash_timer * 4)
            msg_surf = font_small.render(flash_msg, True, (255, 80, 80))
            msg_surf.set_alpha(alpha)
            screen.blit(msg_surf, msg_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

        if game_over:
            draw_game_over(screen, score // 10, coin_total, font_big, font_small)

        pygame.display.flip()

    pygame.quit()


# ── Entry point ──────────────────────────────────────────────────────────────
while True:
    run_game()
