import pygame
import math
import datetime


class MickeysClock:

    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.center = (width // 2, height // 2)

        # Load Mickey hand image
        try:
            self.hand_image = pygame.image.load("images/mickey_hand.png").convert_alpha()
            self.hand_image = pygame.transform.scale(self.hand_image, (40, 120))
        except FileNotFoundError:
            # If image not found, draw a simple hand shape
            self.hand_image = self._create_hand_surface()

        self.font_large = pygame.font.SysFont("Arial", 60, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 28)

    def _create_hand_surface(self):
        """Creates a simple hand surface if image is not available."""
        surf = pygame.Surface((30, 100), pygame.SRCALPHA)
        # Draw arm
        pygame.draw.rect(surf, (255, 220, 185), (10, 20, 10, 70))
        # Draw fist/hand (circle)
        pygame.draw.circle(surf, (255, 220, 185), (15, 15), 15)
        # White glove overlay
        pygame.draw.circle(surf, (255, 255, 255), (15, 12), 13)
        return surf

    def _rotate_hand(self, surface, angle, pivot, offset):

        rotated = pygame.transform.rotate(surface, -angle)
        rect = rotated.get_rect()

        # Calculate position based on angle and offset
        rad = math.radians(angle)
        x = pivot[0] + offset * math.sin(rad) - rect.width // 2
        y = pivot[1] - offset * math.cos(rad) - rect.height // 2
        return rotated, (x, y)

    def draw(self):
        
        now = datetime.datetime.now()
        minutes = now.minute
        seconds = now.second

        # Background
        self.screen.fill((30, 30, 60))

        # Draw clock face circle
        pygame.draw.circle(self.screen, (255, 255, 255), self.center, 200, 3)
        pygame.draw.circle(self.screen, (200, 200, 220), self.center, 8)

        # Draw hour markers
        for i in range(60):
            angle_rad = math.radians(i * 6 - 90)
            if i % 5 == 0:
                length = 185
                width = 3
                color = (255, 255, 255)
            else:
                length = 195
                width = 1
                color = (150, 150, 170)
            x1 = self.center[0] + int(195 * math.cos(angle_rad))
            y1 = self.center[1] + int(195 * math.sin(angle_rad))
            x2 = self.center[0] + int(length * math.cos(angle_rad))
            y2 = self.center[1] + int(length * math.sin(angle_rad))
            pygame.draw.line(self.screen, color, (x1, y1), (x2, y2), width)

        # Calculate angles (0 degrees = 12 o'clock, clockwise)
        minute_angle = minutes * 6        # 360 / 60 = 6 degrees per minute
        second_angle = seconds * 6        # 360 / 60 = 6 degrees per second

        # Draw minute hand (RIGHT hand)
        min_hand, min_pos = self._rotate_hand(self.hand_image, minute_angle, self.center, 60)
        self.screen.blit(min_hand, min_pos)

        # Draw second hand (LEFT hand) - mirrored
        sec_hand = pygame.transform.flip(self.hand_image, True, False)
        sec_hand_rot, sec_pos = self._rotate_hand(sec_hand, second_angle, self.center, 60)
        self.screen.blit(sec_hand_rot, sec_pos)

        # Center dot
        pygame.draw.circle(self.screen, (255, 80, 80), self.center, 10)

        # Display digital time
        time_str = now.strftime("%H:%M:%S")
        time_surface = self.font_large.render(time_str, True, (255, 255, 100))
        time_rect = time_surface.get_rect(center=(self.width // 2, self.height - 60))
        self.screen.blit(time_surface, time_rect)

        # Labels
        min_label = self.font_small.render(f"Minutes: {minutes:02d}", True, (180, 220, 255))
        sec_label = self.font_small.render(f"Seconds: {seconds:02d}", True, (180, 220, 255))
        self.screen.blit(min_label, (20, 20))
        self.screen.blit(sec_label, (20, 55))

        # Legend
        legend_r = self.font_small.render("Right hand = Minutes", True, (200, 255, 200))
        legend_l = self.font_small.render("Left hand  = Seconds", True, (200, 255, 200))
        self.screen.blit(legend_r, (self.width - 260, 20))
        self.screen.blit(legend_l, (self.width - 260, 55))
