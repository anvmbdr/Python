import pygame
import random

# Coin type definitions: name -> (image_file, point_value, spawn_weight, pixel_size)
COIN_TYPES = {
    "bronze": ("images/coin_bronze.png", 1,  60, 28),
    "silver": ("images/coin_silver.png", 3,  30, 34),
    "gold":   ("images/coin_gold.png",   5,  10, 40),
}

# Pre-built list for random.choices() — names and their weights
COIN_NAMES   = list(COIN_TYPES.keys())
COIN_WEIGHTS = [COIN_TYPES[n][2] for n in COIN_NAMES]


def random_coin_type():
    return random.choices(COIN_NAMES, weights=COIN_WEIGHTS, k=1)[0]


class Coin:

    # Fallback colors if image files are missing
    FALLBACK_COLORS = {
        "bronze": (180, 100, 30),
        "silver": (180, 180, 190),
        "gold":   (255, 200, 0),
    }

    def __init__(self, x, y, coin_type=None):
        # Pick a random weighted type if none specified
        self.coin_type = coin_type or random_coin_type()

        name, value, weight, size = COIN_TYPES[self.coin_type]
        self.value = value   # Points awarded when collected
        self.size  = size

        # Load image, fall back to a colored circle
        try:
            img = pygame.image.load(name).convert_alpha()
            self.image = pygame.transform.scale(img, (size, size))
        except Exception:
            self.image = pygame.Surface((size, size), pygame.SRCALPHA)
            color = self.FALLBACK_COLORS[self.coin_type]
            pygame.draw.circle(self.image, color,
                               (size // 2, size // 2), size // 2)
            pygame.draw.circle(self.image, (0, 0, 0),
                               (size // 2, size // 2), size // 2, 2)

        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, speed):
        self.rect.y += speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)
