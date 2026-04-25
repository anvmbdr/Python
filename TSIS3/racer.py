import pygame
import random
import math

PINK = (255, 105, 180)
DEEP_PINK = (220, 20, 120)
WHITE = (255, 255, 255)
BLACK = (10, 5, 15)
DARK = (18, 8, 28)
ROAD_DARK = (30, 18, 42)
ROAD_MID = (40, 25, 55)
LANE_MARK = (255, 210, 80)
GOLD = (255, 220, 80)
RED = (255, 70, 90)
GREEN = (80, 220, 120)
CYAN = (100, 200, 255)
ORANGE = (255, 160, 30)
GRAY = (120, 100, 130)

CAR_COLORS = {
    "pink": (255, 105, 180),
    "mint": (100, 230, 160),
    "lavender": (180, 140, 255),
    "white": (240, 240, 250),
    "red": (255, 80, 80),
}

DIFF_SETTINGS = {
    "easy":   {"base_speed": 4,  "traffic_freq": 180, "obstacle_freq": 220},
    "normal": {"base_speed": 6,  "traffic_freq": 120, "obstacle_freq": 160},
    "hard":   {"base_speed": 9,  "traffic_freq": 80,  "obstacle_freq": 110},
}

POWERUP_TYPES = ["nitro", "shield", "repair"]
COIN_VALUES = [1, 1, 1, 2, 2, 5]


class Road:
    def __init__(self, W, H):
        self.W = W
        self.H = H
        self.num_lanes = 5
        self.margin = 60
        self.road_w = W - self.margin * 2
        self.lane_w = self.road_w // self.num_lanes
        self.scroll = 0
        self.line_h = 60
        self.line_gap = 40
        self.bump_y = -200
        self.bump_active = False
        self.bump_timer = 0
        self.nitro_y = -300
        self.nitro_active = False
        self.nitro_timer = 0

    def lane_center(self, lane):
        return self.margin + lane * self.lane_w + self.lane_w // 2

    def update(self, speed, dt):
        self.scroll = (self.scroll + speed) % (self.line_h + self.line_gap)
        if self.bump_active:
            self.bump_y += speed
            self.bump_timer -= dt
            if self.bump_timer <= 0 or self.bump_y > self.H + 40:
                self.bump_active = False
        if self.nitro_active:
            self.nitro_y += speed
            self.nitro_timer -= dt
            if self.nitro_timer <= 0 or self.nitro_y > self.H + 40:
                self.nitro_active = False

    def try_spawn_event(self, game_time):
        if not self.bump_active and random.random() < 0.003:
            self.bump_y = -40
            self.bump_active = True
            self.bump_timer = 8.0
        if not self.nitro_active and random.random() < 0.002:
            self.nitro_y = -40
            self.nitro_active = True
            self.nitro_timer = 8.0

    def draw(self, surface):
        road_rect = pygame.Rect(self.margin, 0, self.road_w, self.H)
        pygame.draw.rect(surface, ROAD_DARK, road_rect)

        for lane in range(self.num_lanes):
            x = self.margin + lane * self.lane_w
            shade = ROAD_MID if lane % 2 == 0 else ROAD_DARK
            pygame.draw.rect(surface, shade, (x, 0, self.lane_w, self.H))

        for lane in range(1, self.num_lanes):
            x = self.margin + lane * self.lane_w
            y = -self.scroll
            while y < self.H:
                pygame.draw.rect(surface, LANE_MARK, (x - 2, y, 4, self.line_h))
                y += self.line_h + self.line_gap

        pygame.draw.rect(surface, (200, 180, 220), (self.margin - 8, 0, 8, self.H))
        pygame.draw.rect(surface, (200, 180, 220), (self.margin + self.road_w, 0, 8, self.H))

        if self.bump_active:
            by = int(self.bump_y)
            pygame.draw.rect(surface, GRAY, (self.margin, by, self.road_w, 18), border_radius=5)
            for i in range(self.num_lanes):
                cx = self.margin + i * self.lane_w + self.lane_w // 2
                pygame.draw.ellipse(surface, (80, 70, 90), (cx - 20, by + 2, 40, 14))
            lbl = pygame.font.Font(None, 20).render("BUMP", True, WHITE)
            surface.blit(lbl, lbl.get_rect(center=(self.margin + self.road_w // 2, by + 9)))

        if self.nitro_active:
            ny = int(self.nitro_y)
            strip = pygame.Surface((self.road_w, 22), pygame.SRCALPHA)
            strip.fill((255, 220, 0, 100))
            surface.blit(strip, (self.margin, ny))
            pygame.draw.rect(surface, GOLD, (self.margin, ny, self.road_w, 22), 2)
            lbl = pygame.font.Font(None, 20).render("⚡ NITRO STRIP", True, GOLD)
            surface.blit(lbl, lbl.get_rect(center=(self.margin + self.road_w // 2, ny + 11)))


class PlayerCar:
    def __init__(self, road, color_name="pink"):
        self.road = road
        self.lane = 2
        self.W = 32
        self.H = 54
        self.x = road.lane_center(self.lane)
        self.y = road.H - 120
        self.color = CAR_COLORS.get(color_name, CAR_COLORS["pink"])
        self.move_anim = 0
        self.shield_active = False
        self.invincible_timer = 0

    def move(self, direction):
        nl = self.lane + direction
        if 0 <= nl < self.road.num_lanes:
            self.lane = nl
            self.move_anim = 0.15

    def update(self, dt, speed):
        tx = self.road.lane_center(self.lane)
        self.x += (tx - self.x) * min(1.0, dt * 18)
        if self.move_anim > 0:
            self.move_anim -= dt
        if self.invincible_timer > 0:
            self.invincible_timer -= dt

    def get_rect(self):
        return pygame.Rect(int(self.x) - self.W // 2, int(self.y) - self.H // 2, self.W, self.H)

    def draw(self, surface):
        blink = (int(self.invincible_timer * 8) % 2 == 0) if self.invincible_timer > 0 else True
        if not blink:
            return
        x, y = int(self.x), int(self.y)
        col = self.color
        body = pygame.Rect(x - 14, y - 24, 28, 48)
        pygame.draw.rect(surface, col, body, border_radius=8)
        roof = pygame.Rect(x - 10, y - 18, 20, 22)
        pygame.draw.rect(surface, (min(col[0]+40, 255), min(col[1]+40, 255), min(col[2]+40, 255)), roof, border_radius=5)
        pygame.draw.rect(surface, (40, 190, 255, 180), pygame.Rect(x - 9, y - 17, 18, 10), border_radius=3)
        pygame.draw.rect(surface, (255, 255, 120), (x - 12, y - 24, 10, 7), border_radius=3)
        pygame.draw.rect(surface, (255, 255, 120), (x + 2, y - 24, 10, 7), border_radius=3)
        pygame.draw.rect(surface, (255, 80, 80), (x - 12, y + 20, 10, 6), border_radius=2)
        pygame.draw.rect(surface, (255, 80, 80), (x + 2, y + 20, 10, 6), border_radius=2)
        for wx, wy in [(-14, -12), (14, -12), (-14, 14), (14, 14)]:
            pygame.draw.circle(surface, (30, 20, 40), (x + wx, y + wy), 6)
            pygame.draw.circle(surface, (80, 70, 90), (x + wx, y + wy), 4)
        tilt = math.sin(self.move_anim * 20) * 3
        if abs(tilt) > 0.5:
            pass
        if self.shield_active:
            pygame.draw.circle(surface, (100, 200, 255, 120), (x, y), 36, 3)


class TrafficCar:
    COLORS = [(200, 80, 80), (80, 150, 200), (100, 180, 100), (200, 160, 50), (160, 80, 200)]

    def __init__(self, road, speed):
        self.road = road
        self.lane = random.randint(0, road.num_lanes - 1)
        self.x = road.lane_center(self.lane)
        self.y = -60
        self.speed = speed * random.uniform(0.7, 1.1)
        self.color = random.choice(self.COLORS)
        self.W = 30
        self.H = 50

    def update(self, dt):
        self.y += self.speed

    def get_rect(self):
        return pygame.Rect(int(self.x) - self.W // 2, int(self.y) - self.H // 2, self.W, self.H)

    def draw(self, surface):
        x, y = int(self.x), int(self.y)
        col = self.color
        pygame.draw.rect(surface, col, (x - 13, y - 23, 26, 46), border_radius=7)
        pygame.draw.rect(surface, (min(col[0]+30,255), min(col[1]+30,255), min(col[2]+30,255)),
                         (x - 9, y - 17, 18, 20), border_radius=4)
        pygame.draw.rect(surface, (200, 240, 255), (x - 8, y - 16, 16, 9), border_radius=2)
        pygame.draw.rect(surface, (255, 255, 100), (x - 11, y + 18, 8, 6), border_radius=2)
        pygame.draw.rect(surface, (255, 255, 100), (x + 3, y + 18, 8, 6), border_radius=2)
        for wx, wy in [(-13, -10), (13, -10), (-13, 13), (13, 13)]:
            pygame.draw.circle(surface, (25, 20, 35), (x + wx, y + wy), 5)


class Obstacle:
    TYPES = ["oil", "pothole", "barrier"]

    def __init__(self, road, speed):
        self.road = road
        self.lane = random.randint(0, road.num_lanes - 1)
        self.x = road.lane_center(self.lane)
        self.y = -40
        self.speed = speed * 0.5
        self.kind = random.choice(self.TYPES)
        self.W = 36 if self.kind == "barrier" else 30
        self.H = 20 if self.kind == "barrier" else 22

    def update(self, dt):
        self.y += self.speed

    def get_rect(self):
        return pygame.Rect(int(self.x) - self.W // 2, int(self.y) - self.H // 2, self.W, self.H)

    def draw(self, surface):
        x, y = int(self.x), int(self.y)
        if self.kind == "oil":
            pygame.draw.ellipse(surface, (20, 10, 50), (x - 18, y - 10, 36, 20))
            pygame.draw.ellipse(surface, (60, 30, 120, 180), (x - 14, y - 7, 28, 14))
            f = pygame.font.Font(None, 16)
            lbl = f.render("OIL", True, (140, 100, 200))
            surface.blit(lbl, lbl.get_rect(center=(x, y)))
        elif self.kind == "pothole":
            pygame.draw.ellipse(surface, (15, 10, 25), (x - 15, y - 11, 30, 22))
            pygame.draw.ellipse(surface, (35, 25, 48), (x - 11, y - 8, 22, 16))
        elif self.kind == "barrier":
            pygame.draw.rect(surface, (220, 60, 60), (x - 18, y - 9, 36, 18), border_radius=4)
            for i in range(3):
                sx = x - 15 + i * 15
                pygame.draw.rect(surface, (255, 255, 255), (sx, y - 9, 7, 18))


class Coin:
    def __init__(self, road, speed):
        self.road = road
        self.lane = random.randint(0, road.num_lanes - 1)
        self.x = road.lane_center(self.lane)
        self.y = -20
        self.speed = speed * 0.5
        self.value = random.choice(COIN_VALUES)
        self.anim = random.uniform(0, math.pi * 2)

    def update(self, dt):
        self.y += self.speed
        self.anim += dt * 4

    def get_rect(self):
        return pygame.Rect(int(self.x) - 12, int(self.y) - 12, 24, 24)

    def draw(self, surface):
        x, y = int(self.x), int(self.y)
        bob = math.sin(self.anim) * 3
        col = GOLD if self.value <= 2 else (255, 120, 20) if self.value == 5 else GOLD
        pygame.draw.circle(surface, col, (x, int(y + bob)), 11)
        pygame.draw.circle(surface, (min(col[0]+40, 255), min(col[1]+20, 255), 0), (x - 2, int(y + bob) - 2), 5)
        f = pygame.font.Font(None, 16)
        lbl = f.render(str(self.value), True, (40, 20, 0))
        surface.blit(lbl, lbl.get_rect(center=(x, int(y + bob))))


class PowerUp:
    COLORS = {"nitro": (255, 200, 0), "shield": (100, 200, 255), "repair": (100, 255, 150)}
    ICONS = {"nitro": "⚡", "shield": "🛡", "repair": "❤"}

    def __init__(self, road, speed):
        self.road = road
        self.lane = random.randint(0, road.num_lanes - 1)
        self.x = road.lane_center(self.lane)
        self.y = -30
        self.speed = speed * 0.45
        self.kind = random.choice(POWERUP_TYPES)
        self.lifetime = 8.0
        self.anim = 0.0

    def update(self, dt):
        self.y += self.speed
        self.anim += dt * 3
        self.lifetime -= dt

    def get_rect(self):
        return pygame.Rect(int(self.x) - 16, int(self.y) - 16, 32, 32)

    def draw(self, surface):
        x, y = int(self.x), int(self.y)
        col = self.COLORS[self.kind]
        pulse = abs(math.sin(self.anim)) * 4
        pygame.draw.circle(surface, col, (x, y), int(16 + pulse))
        pygame.draw.circle(surface, WHITE, (x, y), int(14 + pulse), 2)
        f = pygame.font.Font(None, 22)
        lbl = f.render(self.kind[:3].upper(), True, (20, 10, 30))
        surface.blit(lbl, lbl.get_rect(center=(x, y)))


class GameSession:
    def __init__(self, W, H, car_color, difficulty):
        self.W = W
        self.H = H
        self.road = Road(W, H)
        self.player = PlayerCar(self.road, car_color)
        self.diff = DIFF_SETTINGS[difficulty]
        self.base_speed = self.diff["base_speed"]
        self.speed = self.base_speed
        self.score = 0
        self.coins = 0
        self.distance = 0.0
        self.traffic = []
        self.obstacles = []
        self.coin_objs = []
        self.powerups = []
        self.active_powerup = None
        self.powerup_timer = 0.0
        self.shield_active = False
        self.traffic_timer = 0
        self.obstacle_timer = 0
        self.coin_timer = 0
        self.powerup_spawn_timer = 0
        self.game_time = 0.0
        self.alive = True
        self.bump_slow_timer = 0.0

    def handle_input(self, keys):
        pass

    def on_key_down(self, key):
        if key == pygame.K_LEFT or key == pygame.K_a:
            self.player.move(-1)
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            self.player.move(1)

    def _safe_spawn_traffic(self):
        lane = random.randint(0, self.road.num_lanes - 1)
        car = TrafficCar(self.road, self.speed)
        car.lane = lane
        car.x = self.road.lane_center(lane)
        pr = self.player.get_rect()
        cr = car.get_rect()
        if abs(car.y - self.player.y) < 120 and car.lane == self.player.lane:
            return None
        return car

    def _safe_spawn_obstacle(self):
        lane = random.randint(0, self.road.num_lanes - 1)
        obs = Obstacle(self.road, self.speed)
        obs.lane = lane
        obs.x = self.road.lane_center(lane)
        if obs.lane == self.player.lane and obs.y < self.player.y + 200:
            return None
        return obs

    def update(self, dt):
        if not self.alive:
            return

        self.game_time += dt

        density = 1 + self.distance / 800
        current_speed = self.speed * density
        if self.bump_slow_timer > 0:
            current_speed *= 0.5
            self.bump_slow_timer -= dt
        if self.active_powerup == "nitro":
            current_speed *= 1.8

        self.road.update(current_speed, dt)
        self.road.try_spawn_event(self.game_time)
        self.player.update(dt, current_speed)
        self.distance += current_speed * dt * 0.8
        self.score = int(self.coins * 10 + self.distance * 0.5)

        if self.active_powerup:
            self.powerup_timer -= dt
            if self.powerup_timer <= 0:
                if self.active_powerup == "shield":
                    self.player.shield_active = False
                    self.shield_active = False
                self.active_powerup = None
                self.powerup_timer = 0

        freq_scale = max(0.4, 1 - self.distance / 1200)
        self.traffic_timer += 1
        if self.traffic_timer >= int(self.diff["traffic_freq"] * freq_scale):
            self.traffic_timer = 0
            tc = self._safe_spawn_traffic()
            if tc:
                self.traffic.append(tc)

        self.obstacle_timer += 1
        if self.obstacle_timer >= int(self.diff["obstacle_freq"] * freq_scale):
            self.obstacle_timer = 0
            obs = self._safe_spawn_obstacle()
            if obs:
                self.obstacles.append(obs)

        self.coin_timer += 1
        if self.coin_timer >= 60:
            self.coin_timer = 0
            self.coin_objs.append(Coin(self.road, current_speed))

        self.powerup_spawn_timer += 1
        if self.powerup_spawn_timer >= 300 and len(self.powerups) == 0 and not self.active_powerup:
            self.powerup_spawn_timer = 0
            self.powerups.append(PowerUp(self.road, current_speed))

        for t in self.traffic:
            t.update(dt)
        for o in self.obstacles:
            o.update(dt)
        for c in self.coin_objs:
            c.update(dt)
        for p in self.powerups:
            p.update(dt)

        self.traffic = [t for t in self.traffic if t.y < self.H + 80]
        self.obstacles = [o for o in self.obstacles if o.y < self.H + 80]
        self.coin_objs = [c for c in self.coin_objs if c.y < self.H + 80]
        self.powerups = [p for p in self.powerups if p.y < self.H + 80 and p.lifetime > 0]

        pr = self.player.get_rect()

        for c in self.coin_objs[:]:
            if pr.colliderect(c.get_rect()):
                self.coins += c.value
                self.score += c.value * 10
                self.coin_objs.remove(c)

        for p in self.powerups[:]:
            if pr.colliderect(p.get_rect()):
                self.apply_powerup(p.kind)
                self.powerups.remove(p)

        if self.player.invincible_timer > 0:
            return

        for t in self.traffic[:]:
            if pr.colliderect(t.get_rect()):
                if self.shield_active:
                    self.shield_active = False
                    self.player.shield_active = False
                    self.active_powerup = None
                    self.powerup_timer = 0
                    self.player.invincible_timer = 2.0
                else:
                    self.alive = False
                return

        for o in self.obstacles[:]:
            if pr.colliderect(o.get_rect()):
                if self.shield_active:
                    self.shield_active = False
                    self.player.shield_active = False
                    self.active_powerup = None
                    self.powerup_timer = 0
                    self.obstacles.remove(o)
                    self.player.invincible_timer = 2.0
                elif self.active_powerup == "repair":
                    self.obstacles.remove(o)
                    self.active_powerup = None
                    self.powerup_timer = 0
                else:
                    if o.kind == "oil":
                        self.bump_slow_timer = 2.0
                    else:
                        self.alive = False
                return

        if self.road.bump_active:
            bump_rect = pygame.Rect(self.road.margin, int(self.road.bump_y) - 9, self.road.road_w, 18)
            if pr.colliderect(bump_rect):
                self.bump_slow_timer = 1.5

        if self.road.nitro_active:
            nitro_rect = pygame.Rect(self.road.margin, int(self.road.nitro_y), self.road.road_w, 22)
            if pr.colliderect(nitro_rect):
                if not self.active_powerup:
                    self.apply_powerup("nitro")

    def apply_powerup(self, kind):
        self.active_powerup = kind
        self.powerup_timer = 4.0
        if kind == "shield":
            self.shield_active = True
            self.player.shield_active = True
        elif kind == "repair":
            self.powerup_timer = 0.1
        elif kind == "nitro":
            self.powerup_timer = 4.0

    def draw(self, surface):
        self.road.draw(surface)
        for t in self.traffic:
            t.draw(surface)
        for o in self.obstacles:
            o.draw(surface)
        for c in self.coin_objs:
            c.draw(surface)
        for p in self.powerups:
            p.draw(surface)
        self.player.draw(surface)
