import pygame

class Ball:

    RADIUS = 25         # Ball radius
    STEP = 20           # Pixels per key press
    COLOR = (220, 30, 30)       # Red
    OUTLINE_COLOR = (255, 100, 100)  # Lighter red for outline

    def __init__(self, x, y, screen_width, screen_height):
        self.x = x
        self.y = y
        self.screen_width = screen_width
        self.screen_height = screen_height

    def move(self, direction):
    
        new_x, new_y = self.x, self.y

        if direction == "up":
            new_y -= self.STEP
        elif direction == "down":
            new_y += self.STEP
        elif direction == "left":
            new_x -= self.STEP
        elif direction == "right":
            new_x += self.STEP

        # Boundary check: ignore move if it goes off-screen
        if self._in_bounds(new_x, new_y):
            self.x = new_x
            self.y = new_y

    def _in_bounds(self, x, y):
        return (
            self.RADIUS <= x <= self.screen_width - self.RADIUS and
            self.RADIUS <= y <= self.screen_height - self.RADIUS
        )

    def draw(self, screen):
        # Shadow
        pygame.draw.circle(screen, (180, 180, 180), (self.x + 4, self.y + 4), self.RADIUS)
        # Main ball
        pygame.draw.circle(screen, self.COLOR, (self.x, self.y), self.RADIUS)
        # Outline
        pygame.draw.circle(screen, self.OUTLINE_COLOR, (self.x, self.y), self.RADIUS, 3)
        # Shine effect
        pygame.draw.circle(screen, (255, 160, 160), (self.x - 8, self.y - 8), 7)
