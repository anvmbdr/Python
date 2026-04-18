import pygame
import sys
import random

# ── Grid & window ─────────────────────────────────────────────────────────────
CELL   = 20
COLS   = 30
ROWS   = 30
WIDTH  = COLS * CELL          # 600 px
HEIGHT = ROWS * CELL + 60     # +60 for HUD bar

# ── Food type definitions ─────────────────────────────────────────────────────
# Each entry: (display_name, color, points, spawn_weight, lifetime_frames)
#   lifetime_frames = how long the food stays before disappearing
#   spawn_weight    = relative probability of this type appearing
FOOD_TYPES = {
    "apple":      ((220,  50,  50), 1,  50, 300),   # common,   lasts 5 s
    "cherry":     ((180,   0, 100), 3,  30, 220),   # uncommon, lasts ~3.7 s
    "blueberry":  (( 60,  60, 200), 5,  15, 160),   # rare,     lasts ~2.7 s
    "golden":     ((255, 200,   0), 10,  5,  90),   # very rare, lasts 1.5 s
}
FOOD_NAMES   = list(FOOD_TYPES.keys())
FOOD_WEIGHTS = [FOOD_TYPES[n][2] for n in FOOD_NAMES]

# ── Game settings ─────────────────────────────────────────────────────────────
FOOD_PER_LEVEL  = 4      # Foods eaten before levelling up
BASE_SPEED_MS   = 180    # Starting move interval (ms)

# ── Colors ────────────────────────────────────────────────────────────────────
BLACK      = (0,   0,   0  )
WHITE      = (255, 255, 255)
SNAKE_HEAD = (100, 255, 120)
SNAKE_BODY = (0,   200,  80)
SNAKE_OUT  = (0,   140,  50)
WALL_COLOR = (70,  70,  70 )
HUD_BG     = (20,  20,  20 )
YELLOW     = (255, 215,   0)
RED        = (220,  50,  50)

# ── Directions ────────────────────────────────────────────────────────────────
UP    = (0,  -1)
DOWN  = (0,   1)
LEFT  = (-1,  0)
RIGHT = (1,   0)


# ── Food class ────────────────────────────────────────────────────────────────

class Food:


    def __init__(self, col, row):
        # Choose food type by weighted probability (task 1)
        self.name = random.choices(FOOD_NAMES, weights=FOOD_WEIGHTS, k=1)[0]
        color, points, weight, lifetime = FOOD_TYPES[self.name]

        self.col     = col
        self.row     = row
        self.color   = color
        self.points  = points
        self.timer   = lifetime   # Countdown in frames (task 2)
        self.visible = True       # Used for blinking effect

    @property
    def pos(self):
        return (self.col, self.row)

    def update(self):
        self.timer -= 1

        # Blink when less than 60 frames remain (~1 second warning)
        if self.timer <= 60:
            self.visible = (self.timer % 12) < 6
        else:
            self.visible = True

        return self.timer > 0   # False = expired, remove it

    def draw(self, screen):
        if not self.visible:
            return  # Skip drawing during blink-off frames

        x = self.col * CELL
        y = self.row * CELL
        rect = pygame.Rect(x + 2, y + 2, CELL - 4, CELL - 4)
        pygame.draw.rect(screen, self.color, rect, border_radius=6)
        # Shine highlight
        pygame.draw.circle(screen, (255, 255, 255), (x + 6, y + 6), 3)

    def draw_label(self, screen, font):
        if not self.visible:
            return
        label = font.render(f"+{self.points}", True, self.color)
        screen.blit(label, (self.col * CELL - 2, self.row * CELL - 14))


# ── Helper functions ──────────────────────────────────────────────────────────

def random_food_pos(snake_body, existing_food_positions):
    occupied = set(snake_body) | set(existing_food_positions)
    while True:
        col = random.randint(1, COLS - 2)
        row = random.randint(1, ROWS - 2)
        if (col, row) not in occupied:
            return col, row


def level_speed(level):
    return max(55, BASE_SPEED_MS - (level - 1) * 18)


# ── Drawing functions ─────────────────────────────────────────────────────────

def draw_grid(screen):
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, (25, 25, 25), (x, 0), (x, ROWS * CELL))
    for y in range(0, ROWS * CELL, CELL):
        pygame.draw.line(screen, (25, 25, 25), (0, y), (WIDTH, y))


def draw_walls(screen):
    for col in range(COLS):
        pygame.draw.rect(screen, WALL_COLOR, (col * CELL, 0, CELL, CELL))
        pygame.draw.rect(screen, WALL_COLOR, (col * CELL, (ROWS-1)*CELL, CELL, CELL))
    for row in range(ROWS):
        pygame.draw.rect(screen, WALL_COLOR, (0, row * CELL, CELL, CELL))
        pygame.draw.rect(screen, WALL_COLOR, ((COLS-1)*CELL, row * CELL, CELL, CELL))


def draw_snake(screen, body):
    for i, (col, row) in enumerate(body):
        color = SNAKE_HEAD if i == 0 else SNAKE_BODY
        rect  = pygame.Rect(col*CELL+1, row*CELL+1, CELL-2, CELL-2)
        pygame.draw.rect(screen, color, rect, border_radius=4)
        pygame.draw.rect(screen, SNAKE_OUT, rect, 1, border_radius=4)


def draw_hud(screen, score, level, eaten, font):
    y = ROWS * CELL
    pygame.draw.rect(screen, HUD_BG, (0, y, WIDTH, 60))
    pygame.draw.line(screen, WALL_COLOR, (0, y), (WIDTH, y), 2)

    score_surf = font.render(f"Score: {score}", True, WHITE)
    level_surf = font.render(f"Level: {level}", True, YELLOW)
    food_surf  = font.render(f"Food: {eaten}/{FOOD_PER_LEVEL}", True, RED)

    screen.blit(score_surf, (15, y + 18))
    screen.blit(level_surf, (WIDTH // 2 - level_surf.get_width() // 2, y + 18))
    screen.blit(food_surf,  (WIDTH - food_surf.get_width() - 15, y + 18))


def draw_legend(screen, font_tiny):
    x, y = WIDTH - 110, 5
    for name in FOOD_NAMES:
        color, pts, *_ = FOOD_TYPES[name]
        pygame.draw.rect(screen, color, (x, y, 12, 12), border_radius=3)
        screen.blit(font_tiny.render(f"{name} +{pts}", True, (180,180,180)),
                    (x + 16, y - 1))
        y += 16


def draw_game_over(screen, score, level, font_big, font_small):
    ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    ov.fill((0, 0, 0, 175))
    screen.blit(ov, (0, 0))
    cy = HEIGHT // 2
    for surf, dy in [
        (font_big.render("GAME OVER", True, RED),           -55),
        (font_small.render(f"Score: {score}  Level: {level}", True, WHITE), 5),
        (font_small.render("R — Restart     Q — Quit", True, (180,180,180)), 50),
    ]:
        screen.blit(surf, surf.get_rect(center=(WIDTH//2, cy+dy)))


def draw_level_up(screen, level, font_big):
    surf = font_big.render(f"LEVEL {level}!", True, YELLOW)
    screen.blit(surf, surf.get_rect(center=(WIDTH//2, HEIGHT//2)))


# ── Main game loop ────────────────────────────────────────────────────────────

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake — Practice 11")
    clock  = pygame.time.Clock()

    font_big  = pygame.font.SysFont("Arial", 40, bold=True)
    font      = pygame.font.SysFont("Arial", 20)
    font_tiny = pygame.font.SysFont("Arial", 13)

    # ── Initial state ─────────────────────────────────────────────────────────
    sc, sr   = COLS // 2, ROWS // 2
    snake    = [(sc, sr), (sc-1, sr), (sc-2, sr)]   # 3 cells long, heading right
    direction = RIGHT
    next_dir  = RIGHT

    # Start with one food item
    foods    = []
    fc, fr   = random_food_pos(snake, [])
    foods.append(Food(fc, fr))

    score         = 0
    level         = 1
    eaten         = 0        # Foods eaten this level
    game_over     = False
    level_up_timer = 0

    move_interval     = level_speed(level)
    last_move_time    = pygame.time.get_ticks()

    # Max simultaneous food items on the board
    MAX_FOOD = 3

    running = True
    while running:
        clock.tick(60)

        # ── Events ────────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit(); sys.exit()
                if game_over:
                    if event.key == pygame.K_r:
                        return
                else:
                    # Prevent reversing direction directly
                    if event.key == pygame.K_UP    and direction != DOWN:
                        next_dir = UP
                    elif event.key == pygame.K_DOWN  and direction != UP:
                        next_dir = DOWN
                    elif event.key == pygame.K_LEFT  and direction != RIGHT:
                        next_dir = LEFT
                    elif event.key == pygame.K_RIGHT and direction != LEFT:
                        next_dir = RIGHT

        # ── Update food timers (task 2) ────────────────────────────────────
        if not game_over:
            # Update each food's countdown; remove expired ones
            for f in foods[:]:
                if not f.update():
                    foods.remove(f)   # Food disappeared after timer ran out

            # Occasionally spawn a new food if board has fewer than MAX_FOOD
            if len(foods) < MAX_FOOD and random.random() < 0.01:
                existing = [f.pos for f in foods]
                nc, nr   = random_food_pos(snake, existing)
                foods.append(Food(nc, nr))

        # ── Snake movement (on timer) ──────────────────────────────────────
        now = pygame.time.get_ticks()
        if not game_over and now - last_move_time >= move_interval:
            last_move_time = now
            direction      = next_dir

            hc = snake[0][0] + direction[0]
            hr = snake[0][1] + direction[1]
            new_head = (hc, hr)

            # Wall collision → game over
            if hc <= 0 or hc >= COLS-1 or hr <= 0 or hr >= ROWS-1:
                game_over = True

            # Self collision → game over
            elif new_head in snake:
                game_over = True

            else:
                snake.insert(0, new_head)   # Move head forward

                # Check if head landed on any food
                ate_food = None
                for f in foods:
                    if f.pos == new_head:
                        ate_food = f
                        break

                if ate_food:
                    foods.remove(ate_food)
                    score  += ate_food.points * 10 * level
                    eaten  += 1
                    # Snake grows (tail not removed)

                    # Spawn replacement food
                    existing = [f.pos for f in foods]
                    nc, nr   = random_food_pos(snake, existing)
                    foods.append(Food(nc, nr))

                    # Level up check
                    if eaten >= FOOD_PER_LEVEL:
                        level         += 1
                        eaten          = 0
                        move_interval  = level_speed(level)   # Speed up
                        level_up_timer = 90

                else:
                    snake.pop()   # Normal move — remove tail

        # ── Draw ──────────────────────────────────────────────────────────────
        screen.fill(BLACK)
        draw_grid(screen)
        draw_walls(screen)

        # Draw all food items (with timers and labels)
        for f in foods:
            f.draw(screen)
            f.draw_label(screen, font_tiny)

        draw_snake(screen, snake)
        draw_legend(screen, font_tiny)
        draw_hud(screen, score, level, eaten, font)

        if level_up_timer > 0:
            draw_level_up(screen, level, font_big)
            level_up_timer -= 1

        if game_over:
            draw_game_over(screen, score, level, font_big, font)

        pygame.display.flip()

    pygame.quit()


# ── Entry point ────────────────────────────────────────────────────────────────
while True:
    run_game()
