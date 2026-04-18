import pygame


class Coin:

    SIZE = 30   # Coin diameter in pixels

    def __init__(self, x, y):
        # Try to load coin image; draw a yellow circle as fallback
        try:
            image = pygame.image.load("images/coin.png").convert_alpha()
            self.image = pygame.transform.scale(image, (self.SIZE, self.SIZE))
        except Exception:
            # Fallback: draw a gold circle
            self.image = pygame.Surface((self.SIZE, self.SIZE), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 215, 0),
                               (self.SIZE // 2, self.SIZE // 2), self.SIZE // 2)
            pygame.draw.circle(self.image, (180, 140, 0),
                               (self.SIZE // 2, self.SIZE // 2), self.SIZE // 2, 2)

        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, speed):
        self.rect.y += speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)
