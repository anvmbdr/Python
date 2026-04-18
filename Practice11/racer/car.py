import pygame


class PlayerCar:

    SPEED = 5   # Pixels per frame the player moves horizontally/vertically

    def __init__(self, x, y):
        # Try to load car image; use a blue rectangle as fallback
        try:
            image = pygame.image.load("images/player_car.png").convert_alpha()
            self.image = pygame.transform.scale(image, (50, 80))
        except Exception:
            self.image = pygame.Surface((50, 80), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (30, 120, 255), (0, 0, 50, 80), border_radius=8)

        # rect is used for position and collision detection
        self.rect = self.image.get_rect(topleft=(x, y))

    def move_left(self):
        self.rect.x -= self.SPEED

    def move_right(self):
        self.rect.x += self.SPEED

    def move_up(self):
        self.rect.y -= self.SPEED

    def move_down(self):
        self.rect.y += self.SPEED

    def clamp(self, left_bound, right_bound):
        self.rect.left  = max(self.rect.left,  left_bound)
        self.rect.right = min(self.rect.right, right_bound)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class EnemyCar:

    def __init__(self, x, y):
        try:
            image = pygame.image.load("images/enemy_car.png").convert_alpha()
            self.image = pygame.transform.scale(image, (50, 80))
        except Exception:
            self.image = pygame.Surface((50, 80), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (220, 40, 40), (0, 0, 50, 80), border_radius=8)

        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, speed):
        self.rect.y += speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)
