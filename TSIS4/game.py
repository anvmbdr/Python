import pygame
import random
from config import *


class Snake:
    def __init__(self, color):
        self.color = color
        self.reset()

    def reset(self):
        cx = GRID_COLS // 2
        cy = GRID_ROWS // 2
        self.body = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.grew = False
        self.shorten_queue = 0

    def set_direction(self, d):
        if (d[0] * -1, d[1] * -1) != self.direction:
            self.next_direction = d

    def move(self):
        self.direction = self.next_direction
        head = (self.body[0][0] + self.direction[0],
                 self.body[0][1] + self.direction[1])
        self.body.insert(0, head)
        if self.grew:
            self.grew = False
        elif self.shorten_queue > 0:
            self.body.pop()
            self.body.pop()
            self.shorten_queue -= 1
        else:
            self.body.pop()

    def grow(self):
        self.grew = True

    def shorten(self, n=2):
        self.shorten_queue += 1
        _ = n

    @property
    def head(self):
        return self.body[0]

    def collides_self(self):
        return self.head in self.body[1:]

    def collides_wall(self):
        x, y = self.head
        return x < 0 or x >= GRID_COLS or y < 0 or y >= GRID_ROWS

    def draw(self, surface):
        for i, seg in enumerate(self.body):
            rect = pygame.Rect(seg[0] * CELL_SIZE, seg[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = self.color if i > 0 else tuple(min(c + 60, 255) for c in self.color)
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)


class FoodItem:
    def __init__(self, pos, kind, spawn_time):
        self.pos = pos
        self.kind = kind
        self.spawn_time = spawn_time
        self.color = FOOD_COLORS[kind]
        self.points = FOOD_POINTS.get(kind, 1)

    def is_expired(self, now):
        return now - self.spawn_time > FOOD_DISAPPEAR_TIME

    def draw(self, surface):
        x, y = self.pos
        rect = pygame.Rect(x * CELL_SIZE + 2, y * CELL_SIZE + 2,
                           CELL_SIZE - 4, CELL_SIZE - 4)
        pygame.draw.ellipse(surface, self.color, rect)


class PowerUp:
    def __init__(self, pos, kind, spawn_time):
        self.pos = pos
        self.kind = kind
        self.spawn_time = spawn_time
        self.color = POWERUP_COLORS[kind]

    def is_expired(self, now):
        return now - self.spawn_time > POWERUP_FIELD_TIME

    def draw(self, surface):
        x, y = self.pos
        cx = x * CELL_SIZE + CELL_SIZE // 2
        cy = y * CELL_SIZE + CELL_SIZE // 2
        points = [
            (cx, cy - CELL_SIZE // 2 + 2),
            (cx + CELL_SIZE // 2 - 2, cy),
            (cx, cy + CELL_SIZE // 2 - 2),
            (cx - CELL_SIZE // 2 + 2, cy),
        ]
        pygame.draw.polygon(surface, self.color, points)


class Game:
    def __init__(self, settings, player_id, personal_best):
        self.settings = settings
        self.player_id = player_id
        self.personal_best = personal_best
        self.snake = Snake(tuple(settings["snake_color"]))
        self.score = 0
        self.level = 1
        self.speed = BASE_SPEED
        self.foods: list[FoodItem] = []
        self.powerup: PowerUp | None = None
        self.obstacles: set = set()
        self.shield_active = False
        self.active_effect: str | None = None
        self.effect_end_time = 0
        self.move_accumulator = 0
        self.running = True
        self.over = False
        self._spawn_food()

    def _occupied(self):
        occupied = set(self.snake.body) | self.obstacles
        for f in self.foods:
            occupied.add(f.pos)
        if self.powerup:
            occupied.add(self.powerup.pos)
        return occupied

    def _random_free_cell(self):
        occupied = self._occupied()
        free = [
            (x, y)
            for x in range(GRID_COLS)
            for y in range(GRID_ROWS)
            if (x, y) not in occupied
        ]
        return random.choice(free) if free else None

    def _spawn_food(self):
        now = pygame.time.get_ticks()
        pos = self._random_free_cell()
        if pos is None:
            return
        kind = random.choices(
            ["normal", "normal", "bonus", "poison"],
            weights=[50, 20, 20, 10]
        )[0]
        self.foods.append(FoodItem(pos, kind, now))

    def _maybe_spawn_powerup(self):
        if self.powerup is not None:
            return
        if random.random() < 0.3:
            pos = self._random_free_cell()
            if pos is None:
                return
            kind = random.choice(["speed", "slow", "shield"])
            self.powerup = PowerUp(pos, kind, pygame.time.get_ticks())

    def _spawn_obstacles(self):
        if self.level < OBSTACLE_START_LEVEL:
            return
        count = OBSTACLES_PER_LEVEL * (self.level - OBSTACLE_START_LEVEL + 1)
        head = self.snake.head
        for _ in range(count * 5):
            if len(self.obstacles) >= count + OBSTACLES_PER_LEVEL * (self.level - OBSTACLE_START_LEVEL):
                break
            pos = self._random_free_cell()
            if pos is None:
                break
            if abs(pos[0] - head[0]) <= 3 and abs(pos[1] - head[1]) <= 3:
                continue
            self.obstacles.add(pos)

    def _apply_powerup(self, kind):
        now = pygame.time.get_ticks()
        self.active_effect = kind
        self.effect_end_time = now + POWERUP_EFFECT_TIME
        if kind == "speed":
            self.speed = BASE_SPEED + (self.level - 1) * SPEED_INCREMENT + 4
        elif kind == "slow":
            self.speed = max(2, BASE_SPEED + (self.level - 1) * SPEED_INCREMENT - 4)
        elif kind == "shield":
            self.shield_active = True

    def _clear_effect(self):
        self.active_effect = None
        self.speed = BASE_SPEED + (self.level - 1) * SPEED_INCREMENT

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            keys = {
                pygame.K_UP:    (0, -1),
                pygame.K_w:     (0, -1),
                pygame.K_DOWN:  (0, 1),
                pygame.K_s:     (0, 1),
                pygame.K_LEFT:  (-1, 0),
                pygame.K_a:     (-1, 0),
                pygame.K_RIGHT: (1, 0),
                pygame.K_d:     (1, 0),
            }
            if event.key in keys:
                self.snake.set_direction(keys[event.key])

    def update(self, dt):
        if self.over:
            return
        now = pygame.time.get_ticks()

        if self.active_effect and now >= self.effect_end_time:
            self._clear_effect()

        self.foods = [f for f in self.foods if not f.is_expired(now)]
        if not self.foods:
            self._spawn_food()

        if self.powerup and self.powerup.is_expired(now):
            self.powerup = None

        self.move_accumulator += dt
        move_interval = 1000 / self.speed
        if self.move_accumulator < move_interval:
            return
        self.move_accumulator -= move_interval

        self.snake.move()
        head = self.snake.head

        wall_hit = self.snake.collides_wall()
        self_hit = self.snake.collides_self()
        obs_hit = head in self.obstacles

        if wall_hit or self_hit or obs_hit:
            if self.shield_active:
                self.shield_active = False
                self.active_effect = None
                if wall_hit:
                    x = max(0, min(GRID_COLS - 1, head[0]))
                    y = max(0, min(GRID_ROWS - 1, head[1]))
                    self.snake.body[0] = (x, y)
                elif obs_hit:
                    self.obstacles.discard(head)
            else:
                self.over = True
                return

        for food in self.foods[:]:
            if food.pos == head:
                self.foods.remove(food)
                if food.kind == "poison":
                    self.snake.shorten(2)
                    if len(self.snake.body) <= 1:
                        self.over = True
                        return
                else:
                    self.score += food.points
                    self.snake.grow()
                    if self.score >= self.level * LEVEL_UP_SCORE:
                        self.level += 1
                        self.speed = BASE_SPEED + (self.level - 1) * SPEED_INCREMENT
                        self._spawn_obstacles()
                        self._maybe_spawn_powerup()
                self._spawn_food()
                break

        if self.powerup and self.powerup.pos == head:
            self._apply_powerup(self.powerup.kind)
            self.powerup = None

    def draw(self, surface):
        surface.fill(BG_COLOR)

        if self.settings.get("grid_overlay"):
            for x in range(0, WINDOW_WIDTH, CELL_SIZE):
                pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT))
            for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
                pygame.draw.line(surface, GRID_COLOR, (0, y), (WINDOW_WIDTH, y))

        for obs in self.obstacles:
            rect = pygame.Rect(obs[0] * CELL_SIZE, obs[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, LIGHT_GRAY, rect)
            pygame.draw.rect(surface, GRAY, rect, 2)

        for food in self.foods:
            food.draw(surface)

        if self.powerup:
            self.powerup.draw(surface)

        self.snake.draw(surface)

        self._draw_hud(surface)

    def _draw_hud(self, surface):
        font_sm = pygame.font.SysFont("consolas", 18)
        font_md = pygame.font.SysFont("consolas", 22, bold=True)

        texts = [
            (f"Score: {self.score}", WHITE),
            (f"Level: {self.level}", WHITE),
            (f"Best:  {self.personal_best}", YELLOW),
        ]
        for i, (txt, color) in enumerate(texts):
            surf = font_md.render(txt, True, color)
            surface.blit(surf, (10, 10 + i * 28))

        if self.shield_active:
            surf = font_sm.render("SHIELD ACTIVE", True, YELLOW)
            surface.blit(surf, (WINDOW_WIDTH - surf.get_width() - 10, 10))
        elif self.active_effect == "speed":
            surf = font_sm.render("SPEED BOOST", True, CYAN)
            surface.blit(surf, (WINDOW_WIDTH - surf.get_width() - 10, 10))
        elif self.active_effect == "slow":
            surf = font_sm.render("SLOW MOTION", True, PURPLE)
            surface.blit(surf, (WINDOW_WIDTH - surf.get_width() - 10, 10))