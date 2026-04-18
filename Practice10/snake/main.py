import pygame
import sys
import random

# ── Constants ────────────────────────────────────────────────────────────────
CELL   = 20          # Size of each grid cell in pixels
COLS   = 30          # Number of columns in the grid
ROWS   = 30          # Number of rows in the grid
WIDTH  = COLS * CELL # Window width  = 600
HEIGHT = ROWS * CELL + 60  # Extra 60px at bottom for HUD

# Colors
BLACK      = (0,   0,   0  )
WHITE      = (255, 255, 255)
GREEN      = (0,   200, 80 )
DARK_GREEN = (0,   140, 50 )
RED        = (220, 50,  50 )
YELLOW     = (255, 215, 0  )
GRAY       = (40,  40,  40 )
WALL_COLOR = (80,  80,  80 )
HUD_COLOR  = (20,  20,  20 )

# Direction vectors (dx, dy)
UP    = (0,  -1)
DOWN  = (0,   1)
LEFT  = (-1,  0)
RIGHT = (1,   0)

# Food needed per level before levelling up
FOOD_PER_LEVEL = 4

# Starting speed (milliseconds between moves); decreases each level
BASE_SPEED = 180


def get_start_speed(level):
    return max(60, BASE_SPEED - (level - 1) * 20)


def random_food(snake_body):
    while True:
        # Playable area: columns 1..COLS-2, rows 1..ROWS-2 (avoid walls)
        col = random.randint(1, COLS - 2)
        row = random.randint(1, ROWS - 2)
        if (col, row) not in snake_body:
            return (col, row)


def draw_grid(screen):
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, (30, 30, 30), (x, 0), (x, ROWS * CELL))
    for y in range(0, ROWS * CELL, CELL):
        pygame.draw.line(screen, (30, 30, 30), (0, y), (WIDTH, y))


def draw_walls(screen):
    # Top and bottom walls
    for col in range(COLS):
        pygame.draw.rect(screen, WALL_COLOR,
                         (col * CELL, 0, CELL, CELL))
        pygame.draw.rect(screen, WALL_COLOR,
                         (col * CELL, (ROWS - 1) * CELL, CELL, CELL))
    # Left and right walls
    for row in range(ROWS):
        pygame.draw.rect(screen, WALL_COLOR,
                         (0, row * CELL, CELL, CELL))
        pygame.draw.rect(screen, WALL_COLOR,
                         ((COLS - 1) * CELL, row * CELL, CELL, CELL))


def draw_snake(screen, snake_body):
    for i, (col, row) in enumerate(snake_body):
        color = GREEN if i > 0 else (100, 255, 120)  # Head is slightly lighter
        rect = pygame.Rect(col * CELL + 1, row * CELL + 1, CELL - 2, CELL - 2)
        pygame.draw.rect(screen, color, rect, border_radius=4)
        # Dark outline
        pygame.draw.rect(screen, DARK_GREEN, rect, 1, border_radius=4)


def draw_food(screen, food_pos):
    col, row = food_pos
    rect = pygame.Rect(col * CELL + 2, row * CELL + 2, CELL - 4, CELL - 4)
    pygame.draw.rect(screen, RED, rect, border_radius=6)
    # Shine dot
    pygame.draw.circle(screen, (255, 140, 140),
                       (col * CELL + 6, row * CELL + 6), 3)


def draw_hud(screen, score, level, food_count, font):
    hud_y = ROWS * CELL
    pygame.draw.rect(screen, HUD_COLOR, (0, hud_y, WIDTH, 60))
    pygame.draw.line(screen, WALL_COLOR, (0, hud_y), (WIDTH, hud_y), 2)

    score_surf = font.render(f"Score: {score}", True, WHITE)
    level_surf = font.render(f"Level: {level}", True, YELLOW)
    food_surf  = font.render(f"Food: {food_count}/{FOOD_PER_LEVEL}", True, RED)

    screen.blit(score_surf, (15,  hud_y + 18))
    screen.blit(level_surf, (WIDTH // 2 - level_surf.get_width() // 2, hud_y + 18))
    screen.blit(food_surf,  (WIDTH - food_surf.get_width() - 15, hud_y + 18))


def draw_game_over(screen, score, level, font_big, font_small):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    over_s  = font_big.render("GAME OVER", True, RED)
    score_s = font_small.render(f"Score: {score}   Level: {level}", True, WHITE)
    retry_s = font_small.render("R — Restart     Q — Quit", True, (180, 180, 180))

    cy = HEIGHT // 2
    screen.blit(over_s,  over_s.get_rect(center=(WIDTH // 2, cy - 50)))
    screen.blit(score_s, score_s.get_rect(center=(WIDTH // 2, cy + 10)))
    screen.blit(retry_s, retry_s.get_rect(center=(WIDTH // 2, cy + 55)))


def draw_level_up(screen, level, font_big):
    surf = font_big.render(f"LEVEL {level}!", True, YELLOW)
    screen.blit(surf, surf.get_rect(center=(WIDTH // 2, HEIGHT // 2)))


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    font_big   = pygame.font.SysFont("Arial", 40, bold=True)
    font_small = pygame.font.SysFont("Arial", 22)

    # ── Initial game state ───────────────────────────────────────────────────
    # Snake starts in the middle, 3 cells long, moving right
    start_col, start_row = COLS // 2, ROWS // 2
    snake = [(start_col, start_row),
             (start_col - 1, start_row),
             (start_col - 2, start_row)]

    direction  = RIGHT   # Current movement direction
    next_dir   = RIGHT   # Queued direction (applied on next move)
    food       = random_food(set(snake))  # First food position

    score      = 0
    level      = 1
    food_count = 0       # Foods eaten this level
    game_over  = False
    level_up_timer = 0   # Frames to show level-up banner

    # Movement timer: snake moves every `move_interval` milliseconds
    move_interval = get_start_speed(level)
    last_move_time = pygame.time.get_ticks()

    running = True
    while running:
        clock.tick(60)  # Render at 60 FPS, but snake moves on its own timer

        # ── Events ──────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if game_over:
                    if event.key == pygame.K_r:
                        return  # Restart
                else:
                    # Change direction — cannot reverse directly
                    if event.key == pygame.K_UP    and direction != DOWN:
                        next_dir = UP
                    elif event.key == pygame.K_DOWN  and direction != UP:
                        next_dir = DOWN
                    elif event.key == pygame.K_LEFT  and direction != RIGHT:
                        next_dir = LEFT
                    elif event.key == pygame.K_RIGHT and direction != LEFT:
                        next_dir = RIGHT

        # ── Update (on move timer) ───────────────────────────────────────────
        now = pygame.time.get_ticks()
        if not game_over and now - last_move_time >= move_interval:
            last_move_time = now
            direction = next_dir  # Apply queued direction

            # Calculate new head position
            head_col = snake[0][0] + direction[0]
            head_row = snake[0][1] + direction[1]
            new_head = (head_col, head_row)

            # 1. Wall collision — hitting the border kills the snake
            if (head_col <= 0 or head_col >= COLS - 1 or
                    head_row <= 0 or head_row >= ROWS - 1):
                game_over = True

            # 2. Self collision — hitting own body kills the snake
            elif new_head in snake:
                game_over = True

            else:
                # Move snake: add new head at front
                snake.insert(0, new_head)

                if new_head == food:
                    # Ate food: grow (don't remove tail), update counters
                    score      += 10 * level  # More points at higher levels
                    food_count += 1

                    # Spawn new food not on wall or snake body (task 2)
                    food = random_food(set(snake))

                    # Check for level up (task 3)
                    if food_count >= FOOD_PER_LEVEL:
                        level      += 1
                        food_count  = 0
                        move_interval = get_start_speed(level)  # Speed up (task 4)
                        level_up_timer = 90  # Show banner for 90 frames
                else:
                    # Normal move: remove tail so snake stays same length
                    snake.pop()

        # ── Draw ────────────────────────────────────────────────────────────
        screen.fill(BLACK)
        draw_grid(screen)
        draw_walls(screen)
        draw_food(screen, food)
        draw_snake(screen, snake)
        draw_hud(screen, score, level, food_count, font_small)  # Task 5

        # Show level-up banner briefly
        if level_up_timer > 0:
            draw_level_up(screen, level, font_big)
            level_up_timer -= 1

        if game_over:
            draw_game_over(screen, score, level, font_big, font_small)

        pygame.display.flip()

    pygame.quit()


# ── Entry point ──────────────────────────────────────────────────────────────
while True:
    run_game()
