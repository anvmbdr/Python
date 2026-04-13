import pygame
import sys
from ball import Ball

# Window settings
WIDTH, HEIGHT = 700, 600
FPS = 60
TITLE = "Moving Ball Game"

# Colors
BG_COLOR    = (245, 245, 245)   # White background
GRID_COLOR  = (220, 220, 220)
TEXT_COLOR  = (50, 50, 50)
ACCENT      = (100, 150, 255)


def draw_grid(screen):
    for x in range(0, WIDTH, 40):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y), 1)


def draw_hud(screen, ball, font):
    pos_text = font.render(f"Position: ({ball.x}, {ball.y})", True, TEXT_COLOR)
    screen.blit(pos_text, (10, 10))

    hint = font.render("Arrow keys: Move   R: Reset   Q: Quit", True, ACCENT)
    screen.blit(hint, (10, HEIGHT - 30))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial", 20)

    # Create ball at center of screen
    ball = Ball(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ball.move("up")
                elif event.key == pygame.K_DOWN:
                    ball.move("down")
                elif event.key == pygame.K_LEFT:
                    ball.move("left")
                elif event.key == pygame.K_RIGHT:
                    ball.move("right")
                elif event.key == pygame.K_r:
                    # Reset ball to center
                    ball.x = WIDTH // 2
                    ball.y = HEIGHT // 2
                elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                    running = False

        # Draw
        screen.fill(BG_COLOR)
        draw_grid(screen)
        ball.draw(screen)
        draw_hud(screen, ball, font)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
