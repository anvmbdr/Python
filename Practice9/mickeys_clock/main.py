import pygame
import sys
from clock import MickeysClock

# Window settings
WIDTH, HEIGHT = 700, 600
FPS = 60
TITLE = "Mickey's Clock"


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock_tick = pygame.time.Clock()

    # Create clock object
    mickey_clock = MickeysClock(screen, WIDTH, HEIGHT)

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    running = False

        # Draw clock
        mickey_clock.draw()

        pygame.display.flip()
        clock_tick.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
