import pygame
import sys
import math

# ── Constants ────────────────────────────────────────────────────────────────
CANVAS_W       = 900
TOOLBAR_H      = 80
WIN_W          = CANVAS_W
WIN_H          = 600 + TOOLBAR_H

# Colors
WHITE          = (255, 255, 255)
BLACK          = (0,   0,   0  )
BG_COLOR       = (255, 255, 255)   # Canvas background
TOOLBAR_BG     = (40,  40,  40 )
SELECTED_RING  = (255, 255,  0 )

# 20-color palette (task 4)
PALETTE = [
    (0,   0,   0  ),  (255,255,255),  (200,  0,  0 ),  (0,  180,  0 ),
    (0,   0, 220  ),  (255,165,  0),  (255, 255,  0 ),  (128,  0,128 ),
    (0,  200, 200 ),  (255,105,180),  (139, 69, 19  ),  (128,128,128 ),
    (200,200, 200 ),  (0,  100,  0),  (0,    0,100  ),  (100,  0,  0 ),
    (255,215,   0 ),  (75,  0, 130),  (173,216,230  ),  (144,238,144 ),
]

# Tool names
PENCIL    = "pencil"
RECTANGLE = "rectangle"
CIRCLE    = "circle"
ERASER    = "eraser"
TOOLS     = [PENCIL, RECTANGLE, CIRCLE, ERASER]
TOOL_LABELS = ["Pencil", "Rect", "Circle", "Eraser"]
TOOL_COLORS = [(100,100,100), (80,80,160), (160,80,80), (80,160,80)]


def tool_rect(i):
    
    return pygame.Rect(10 + i * 75, 10, 65, 60)

def color_rect(i):
    
    return pygame.Rect(340 + (i % 10) * 32, 8 + (i // 10) * 32, 28, 28)

def minus_rect():
    return pygame.Rect(820, 25, 30, 30)

def plus_rect():
    return pygame.Rect(858, 25, 30, 30)

def clear_rect():
    return pygame.Rect(WIN_W - 90, 20, 80, 40)


def draw_toolbar(screen, font, font_big, cur_tool, cur_color, brush_size):
    
    pygame.draw.rect(screen, TOOLBAR_BG, (0, 0, WIN_W, TOOLBAR_H))

    # Tool buttons
    for i, (label, color) in enumerate(zip(TOOL_LABELS, TOOL_COLORS)):
        r = tool_rect(i)
        border = SELECTED_RING if TOOLS[i] == cur_tool else (80, 80, 80)
        pygame.draw.rect(screen, color, r, border_radius=8)
        pygame.draw.rect(screen, border, r, 3, border_radius=8)
        surf = font.render(label, True, WHITE)
        screen.blit(surf, surf.get_rect(center=r.center))

    # Color palette
    for i, c in enumerate(PALETTE):
        r = color_rect(i)
        pygame.draw.rect(screen, c, r, border_radius=4)
        if c == cur_color:
            pygame.draw.rect(screen, SELECTED_RING, r, 3, border_radius=4)

    # Current color preview box
    preview = pygame.Rect(318, 20, 16, 40)
    pygame.draw.rect(screen, cur_color, preview, border_radius=3)
    pygame.draw.rect(screen, WHITE, preview, 1, border_radius=3)

    # Brush size
    size_surf = font.render(f"Size:{brush_size}", True, WHITE)
    screen.blit(size_surf, (790, 8))
    pygame.draw.rect(screen, (80, 80, 80), minus_rect(), border_radius=4)
    pygame.draw.rect(screen, (80, 80, 80), plus_rect(),  border_radius=4)
    screen.blit(font_big.render("-", True, WHITE), (minus_rect().x + 8, minus_rect().y + 3))
    screen.blit(font_big.render("+", True, WHITE), (plus_rect().x  + 6, plus_rect().y  + 3))

    # Clear button
    cr = clear_rect()
    pygame.draw.rect(screen, (160, 50, 50), cr, border_radius=6)
    cl = font.render("Clear", True, WHITE)
    screen.blit(cl, cl.get_rect(center=cr.center))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Paint")
    clock  = pygame.time.Clock()

    font     = pygame.font.SysFont("Arial", 14, bold=True)
    font_big = pygame.font.SysFont("Arial", 18, bold=True)

    # Canvas surface (what gets drawn on)
    canvas = pygame.Surface((WIN_W, WIN_H - TOOLBAR_H))
    canvas.fill(BG_COLOR)

    # Preview overlay for shapes (transparent)
    preview = pygame.Surface((WIN_W, WIN_H - TOOLBAR_H), pygame.SRCALPHA)

    cur_tool   = PENCIL
    cur_color  = PALETTE[0]      # start with black
    brush_size = 5

    drawing    = False
    start_pos  = None
    last_pos   = None

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                if my < TOOLBAR_H:
                    # ── Toolbar click ────────────────────────────────────
                    for i, tool in enumerate(TOOLS):
                        if tool_rect(i).collidepoint(mx, my):
                            cur_tool = tool

                    for i, c in enumerate(PALETTE):
                        if color_rect(i).collidepoint(mx, my):
                            cur_color = c
                            if cur_tool == ERASER:
                                cur_tool = PENCIL

                    if minus_rect().collidepoint(mx, my):
                        brush_size = max(1, brush_size - 1)
                    if plus_rect().collidepoint(mx, my):
                        brush_size = min(60, brush_size + 1)
                    if clear_rect().collidepoint(mx, my):
                        canvas.fill(BG_COLOR)

                else:
                    # ── Canvas click ─────────────────────────────────────
                    cx, cy = mx, my - TOOLBAR_H
                    drawing   = True
                    start_pos = (cx, cy)
                    last_pos  = (cx, cy)

                    if cur_tool in (PENCIL, ERASER):
                        color = BG_COLOR if cur_tool == ERASER else cur_color
                        pygame.draw.circle(canvas, color, (cx, cy), brush_size)

            elif event.type == pygame.MOUSEBUTTONUP:
                if drawing and start_pos is not None:
                    mx, my = event.pos
                    cx, cy = mx, my - TOOLBAR_H
                    sx, sy = start_pos

                    # Commit rectangle (task 1)
                    if cur_tool == RECTANGLE:
                        r = pygame.Rect(min(sx,cx), min(sy,cy), abs(cx-sx), abs(cy-sy))
                        pygame.draw.rect(canvas, cur_color, r)

                    # Commit circle (task 2)
                    elif cur_tool == CIRCLE:
                        radius = int(math.hypot(cx - sx, cy - sy))
                        if radius > 0:
                            pygame.draw.circle(canvas, cur_color, (sx, sy), radius)

                drawing   = False
                start_pos = None
                last_pos  = None
                preview.fill((0, 0, 0, 0))  # clear preview

            elif event.type == pygame.MOUSEMOTION:
                mx, my = event.pos
                if drawing and my >= TOOLBAR_H:
                    cx, cy = mx, my - TOOLBAR_H

                    if cur_tool in (PENCIL, ERASER):
                        # Draw continuous stroke
                        color = BG_COLOR if cur_tool == ERASER else cur_color
                        if last_pos:
                            pygame.draw.line(canvas, color, last_pos, (cx,cy), brush_size*2)
                        pygame.draw.circle(canvas, color, (cx,cy), brush_size)
                        last_pos = (cx, cy)

                    else:
                        # Live shape preview
                        preview.fill((0, 0, 0, 0))
                        sx, sy = start_pos
                        pr, pg, pb = cur_color

                        if cur_tool == RECTANGLE:
                            r = pygame.Rect(min(sx,cx), min(sy,cy), abs(cx-sx), abs(cy-sy))
                            pygame.draw.rect(preview, (pr,pg,pb,200), r, 2)

                        elif cur_tool == CIRCLE:
                            radius = int(math.hypot(cx-sx, cy-sy))
                            if radius > 0:
                                pygame.draw.circle(preview, (pr,pg,pb,200), (sx,sy), radius, 2)

        # ── Render ──────────────────────────────────────────────────────────
        screen.fill((20, 20, 20))
        screen.blit(canvas, (0, TOOLBAR_H))
        screen.blit(preview, (0, TOOLBAR_H))
        draw_toolbar(screen, font, font_big, cur_tool, cur_color, brush_size)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
