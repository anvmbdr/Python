import pygame
import sys
import math

# ── Window ────────────────────────────────────────────────────────────────────
WIN_W      = 900
TOOLBAR_H  = 80
WIN_H      = 600 + TOOLBAR_H

# ── Colors ────────────────────────────────────────────────────────────────────
WHITE         = (255, 255, 255)
BLACK         = (0,   0,   0  )
BG_COLOR      = (255, 255, 255)
TOOLBAR_BG    = (40,  40,  40 )
SELECTED_RING = (255, 255,  0 )

# 20-color palette
PALETTE = [
    (0,   0,   0  ), (255,255,255), (200,  0,  0), (  0,180,  0),
    (0,   0, 220  ), (255,165,  0), (255,255,  0), (128,  0,128),
    (0,  200, 200 ), (255,105,180), (139, 69, 19), (128,128,128),
    (200,200, 200 ), (  0,100,  0), (  0,  0,100), (100,  0,  0),
    (255,215,   0 ), ( 75,  0,130), (173,216,230), (144,238,144),
]

# All available tools (Practice 10 + Practice 11 additions)
TOOLS = [
    "pencil",      # freehand drawing
    "eraser",      # paints with background color
    "rectangle",   # click-drag axis-aligned rectangle  (P10)
    "circle",      # click-drag circle                  (P10)
    "square",      # click-drag perfect square          (P11 task 1)
    "rtriangle",   # right triangle                     (P11 task 2)
    "etriangle",   # equilateral triangle               (P11 task 3)
    "rhombus",     # rhombus (diamond)                  (P11 task 4)
]
TOOL_LABELS = ["Pencil","Eraser","Rect","Circle","Square","R.Tri","Eq.Tri","Rhombus"]
TOOL_COLORS = [
    (100,100,100),(80,140,80),(80,80,160),(160,80,80),
    (80,130,160),(140,100,60),(100,140,60),(130,80,140),
]

SHAPE_TOOLS = {"rectangle","circle","square","rtriangle","etriangle","rhombus"}


# ── Toolbar geometry helpers ──────────────────────────────────────────────────

def tool_rect(i):
    
    col = i % 4
    row = i // 4
    return pygame.Rect(10 + col * 72, 5 + row * 36, 68, 32)

def color_rect(i):
    
    return pygame.Rect(310 + (i % 10) * 28, 6 + (i // 10) * 28, 24, 24)

def minus_rect():
    return pygame.Rect(620, 28, 26, 26)

def plus_rect():
    return pygame.Rect(650, 28, 26, 26)

def clear_rect():
    return pygame.Rect(WIN_W - 80, 24, 72, 34)

def fill_toggle_rect():
    return pygame.Rect(690, 10, 80, 28)


# ── Shape drawing helpers ─────────────────────────────────────────────────────

def draw_square(surface, color, sx, sy, ex, ey, fill, line_w):
    
    side = min(abs(ex - sx), abs(ey - sy))
    dx   = side if ex >= sx else -side
    dy   = side if ey >= sy else -side
    rect = pygame.Rect(min(sx, sx+dx), min(sy, sy+dy), side, side)
    if fill:
        pygame.draw.rect(surface, color, rect)
    else:
        pygame.draw.rect(surface, color, rect, line_w)


def draw_right_triangle(surface, color, sx, sy, ex, ey, fill, line_w):
    
    points = [(sx, sy), (ex, sy), (sx, ey)]
    if fill:
        pygame.draw.polygon(surface, color, points)
    else:
        pygame.draw.polygon(surface, color, points, line_w)


def draw_equilateral_triangle(surface, color, sx, sy, ex, ey, fill, line_w):
    
    base   = abs(ex - sx)
    if base < 2:
        return
    height = int(base * math.sqrt(3) / 2)
    mid_x  = (sx + ex) // 2

    # Apex is above the base (or below if dragged upward)
    if ey < sy:
        apex_y = ey + height
        base_y = ey
    else:
        apex_y = ey - height
        base_y = ey

    points = [(sx, base_y), (ex, base_y), (mid_x, apex_y)]
    if fill:
        pygame.draw.polygon(surface, color, points)
    else:
        pygame.draw.polygon(surface, color, points, line_w)


def draw_rhombus(surface, color, sx, sy, ex, ey, fill, line_w):
    
    cx = (sx + ex) // 2   # centre x
    cy = (sy + ey) // 2   # centre y
    points = [(cx, sy), (ex, cy), (cx, ey), (sx, cy)]
    if fill:
        pygame.draw.polygon(surface, color, points)
    else:
        pygame.draw.polygon(surface, color, points, line_w)


# ── Toolbar drawing ───────────────────────────────────────────────────────────

def draw_toolbar(screen, font, font_big,
                 cur_tool, cur_color, brush_size, fill_shapes):

    pygame.draw.rect(screen, TOOLBAR_BG, (0, 0, WIN_W, TOOLBAR_H))

    # Tool buttons
    for i, (label, color) in enumerate(zip(TOOL_LABELS, TOOL_COLORS)):
        r      = tool_rect(i)
        border = SELECTED_RING if TOOLS[i] == cur_tool else (70, 70, 70)
        pygame.draw.rect(screen, color, r, border_radius=6)
        pygame.draw.rect(screen, border, r, 2, border_radius=6)
        s = font.render(label, True, WHITE)
        screen.blit(s, s.get_rect(center=r.center))

    # Color palette
    for i, c in enumerate(PALETTE):
        r = color_rect(i)
        pygame.draw.rect(screen, c, r, border_radius=3)
        if c == cur_color:
            pygame.draw.rect(screen, SELECTED_RING, r, 2, border_radius=3)

    # Current color preview
    pv = pygame.Rect(306, 18, 12, 44)
    pygame.draw.rect(screen, cur_color, pv, border_radius=2)
    pygame.draw.rect(screen, WHITE, pv, 1, border_radius=2)

    # Brush size controls
    screen.blit(font.render(f"Sz:{brush_size}", True, WHITE), (600, 10))
    for r, lbl in [(minus_rect(), "-"), (plus_rect(), "+")]:
        pygame.draw.rect(screen, (80, 80, 80), r, border_radius=4)
        screen.blit(font_big.render(lbl, True, WHITE),
                    (r.x + (6 if lbl == "-" else 5), r.y + 2))

    # Fill toggle button (filled vs outline shapes)
    fr    = fill_toggle_rect()
    f_col = (60, 130, 60) if fill_shapes else (80, 80, 80)
    pygame.draw.rect(screen, f_col, fr, border_radius=5)
    pygame.draw.rect(screen, WHITE, fr, 1, border_radius=5)
    screen.blit(font.render("Fill" if fill_shapes else "Outline", True, WHITE),
                font.render("Fill" if fill_shapes else "Outline", True, WHITE)
                .get_rect(center=fr.center))

    # Clear button
    cr = clear_rect()
    pygame.draw.rect(screen, (160, 50, 50), cr, border_radius=5)
    screen.blit(font.render("Clear", True, WHITE),
                font.render("Clear", True, WHITE).get_rect(center=cr.center))


# ── Preview helper ────────────────────────────────────────────────────────────

def render_shape_preview(preview_surf, tool, cur_color,
                          sx, sy, mx, my, fill, line_w):
    
    preview_surf.fill((0, 0, 0, 0))
    pr, pg, pb = cur_color
    alpha_color = (pr, pg, pb, 160)   # semi-transparent version

    if tool == "rectangle":
        r = pygame.Rect(min(sx,mx), min(sy,my), abs(mx-sx), abs(my-sy))
        pygame.draw.rect(preview_surf, alpha_color, r, 0 if fill else line_w)

    elif tool == "circle":
        radius = int(math.hypot(mx-sx, my-sy))
        if radius > 0:
            pygame.draw.circle(preview_surf, alpha_color, (sx,sy), radius,
                               0 if fill else line_w)

    elif tool == "square":
        side = min(abs(mx-sx), abs(my-sy))
        dx   = side if mx >= sx else -side
        dy   = side if my >= sy else -side
        r    = pygame.Rect(min(sx, sx+dx), min(sy, sy+dy), side, side)
        pygame.draw.rect(preview_surf, alpha_color, r, 0 if fill else line_w)

    elif tool == "rtriangle":
        pts = [(sx, sy), (mx, sy), (sx, my)]
        pygame.draw.polygon(preview_surf, alpha_color, pts, 0 if fill else line_w)

    elif tool == "etriangle":
        base   = abs(mx - sx)
        if base >= 2:
            height = int(base * math.sqrt(3) / 2)
            mid_x  = (sx + mx) // 2
            apex_y = (my + height) if my < sy else (my - height)
            pts    = [(sx, my), (mx, my), (mid_x, apex_y)]
            pygame.draw.polygon(preview_surf, alpha_color, pts, 0 if fill else line_w)

    elif tool == "rhombus":
        cx, cy = (sx+mx)//2, (sy+my)//2
        pts = [(cx, sy), (mx, cy), (cx, my), (sx, cy)]
        pygame.draw.polygon(preview_surf, alpha_color, pts, 0 if fill else line_w)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Paint — Practice 11")
    clock  = pygame.time.Clock()

    font     = pygame.font.SysFont("Arial", 13, bold=True)
    font_big = pygame.font.SysFont("Arial", 17, bold=True)

    # Canvas: permanent drawing surface
    canvas  = pygame.Surface((WIN_W, WIN_H - TOOLBAR_H))
    canvas.fill(BG_COLOR)

    # Preview overlay: temporary, redrawn every frame while dragging
    preview = pygame.Surface((WIN_W, WIN_H - TOOLBAR_H), pygame.SRCALPHA)

    cur_tool    = "pencil"
    cur_color   = PALETTE[0]     # Start with black
    brush_size  = 5
    fill_shapes = True           # Filled shapes by default

    drawing    = False
    start_pos  = None            # Canvas-space coordinates of mouse-down
    last_pos   = None            # Previous pencil position for smooth strokes

    LINE_W = 2   # Outline width for non-filled shapes

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
                    # ── Toolbar interactions ─────────────────────────────
                    for i, t in enumerate(TOOLS):
                        if tool_rect(i).collidepoint(mx, my):
                            cur_tool = t

                    for i, c in enumerate(PALETTE):
                        if color_rect(i).collidepoint(mx, my):
                            cur_color = c
                            if cur_tool == "eraser":
                                cur_tool = "pencil"

                    if minus_rect().collidepoint(mx, my):
                        brush_size = max(1, brush_size - 1)
                    if plus_rect().collidepoint(mx, my):
                        brush_size = min(60, brush_size + 1)
                    if clear_rect().collidepoint(mx, my):
                        canvas.fill(BG_COLOR)
                    if fill_toggle_rect().collidepoint(mx, my):
                        fill_shapes = not fill_shapes

                else:
                    # ── Start drawing on canvas ──────────────────────────
                    cx, cy    = mx, my - TOOLBAR_H
                    drawing   = True
                    start_pos = (cx, cy)
                    last_pos  = (cx, cy)

                    if cur_tool in ("pencil", "eraser"):
                        color = BG_COLOR if cur_tool == "eraser" else cur_color
                        pygame.draw.circle(canvas, color, (cx, cy), brush_size)

            elif event.type == pygame.MOUSEBUTTONUP:
                if drawing and start_pos:
                    mx, my = event.pos
                    cx, cy = mx, my - TOOLBAR_H
                    sx, sy = start_pos

                    # Commit the final shape to the canvas
                    if cur_tool == "rectangle":
                        r = pygame.Rect(min(sx,cx), min(sy,cy), abs(cx-sx), abs(cy-sy))
                        pygame.draw.rect(canvas, cur_color, r,
                                         0 if fill_shapes else LINE_W)

                    elif cur_tool == "circle":
                        radius = int(math.hypot(cx-sx, cy-sy))
                        if radius > 0:
                            pygame.draw.circle(canvas, cur_color, (sx, sy), radius,
                                               0 if fill_shapes else LINE_W)

                    elif cur_tool == "square":
                        draw_square(canvas, cur_color, sx, sy, cx, cy,
                                    fill_shapes, LINE_W)

                    elif cur_tool == "rtriangle":
                        # Task 2: right triangle
                        draw_right_triangle(canvas, cur_color, sx, sy, cx, cy,
                                            fill_shapes, LINE_W)

                    elif cur_tool == "etriangle":
                        # Task 3: equilateral triangle
                        draw_equilateral_triangle(canvas, cur_color, sx, sy, cx, cy,
                                                  fill_shapes, LINE_W)

                    elif cur_tool == "rhombus":
                        # Task 4: rhombus
                        draw_rhombus(canvas, cur_color, sx, sy, cx, cy,
                                     fill_shapes, LINE_W)

                    preview.fill((0, 0, 0, 0))  # Clear preview after commit

                drawing   = False
                start_pos = None
                last_pos  = None

            elif event.type == pygame.MOUSEMOTION:
                mx, my = event.pos
                if drawing and my >= TOOLBAR_H:
                    cx, cy = mx, my - TOOLBAR_H

                    if cur_tool in ("pencil", "eraser"):
                        # Continuous freehand stroke
                        color = BG_COLOR if cur_tool == "eraser" else cur_color
                        if last_pos:
                            pygame.draw.line(canvas, color, last_pos, (cx,cy),
                                             brush_size * 2)
                        pygame.draw.circle(canvas, color, (cx, cy), brush_size)
                        last_pos = (cx, cy)

                    elif cur_tool in SHAPE_TOOLS:
                        # Update live preview for shape tools
                        sx, sy = start_pos
                        render_shape_preview(preview, cur_tool, cur_color,
                                             sx, sy, cx, cy, fill_shapes, LINE_W)

        # ── Render ────────────────────────────────────────────────────────────
        screen.fill((20, 20, 20))
        screen.blit(canvas,  (0, TOOLBAR_H))
        screen.blit(preview, (0, TOOLBAR_H))    # Shape preview on top
        draw_toolbar(screen, font, font_big,
                     cur_tool, cur_color, brush_size, fill_shapes)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
