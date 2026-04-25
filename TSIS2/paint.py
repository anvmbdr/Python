import pygame
import sys
from datetime import datetime
from tools import (
    draw_pencil, draw_line, draw_rectangle, draw_square,
    draw_circle, draw_right_triangle, draw_equilateral_triangle,
    draw_rhombus, flood_fill
)

pygame.init()

SCREEN_W, SCREEN_H = 1150, 720
TOOLBAR_W = 170
CANVAS_W = SCREEN_W - TOOLBAR_W
CANVAS_H = SCREEN_H

WHITE = (255, 255, 255)
BLACK = (10, 10, 10)
BG = (18, 28, 22)
PANEL = (24, 38, 30)
BTN = (35, 58, 44)
BTN_ACTIVE = (72, 175, 100)
BTN_HOVER = (50, 80, 60)
TEXT_CLR = (200, 230, 210)
DIM = (90, 120, 100)
BORDER = (45, 75, 55)

COLORS = [
    (10, 10, 10), (255, 255, 255), (210, 55, 55), (55, 190, 85),
    (50, 110, 220), (230, 195, 40), (210, 105, 25), (165, 60, 210),
    (0, 185, 205), (225, 115, 165), (110, 65, 30), (155, 155, 155),
    (255, 140, 0), (0, 128, 128), (128, 0, 64), (64, 64, 128),
]

TOOLS = [
    "pencil", "line", "rect", "square",
    "circle", "rtriangle", "etriangle", "rhombus",
    "fill", "eraser", "text"
]

TOOL_LABELS = {
    "pencil":    "Pencil",
    "line":      "Line",
    "rect":      "Rectangle",
    "square":    "Square",
    "circle":    "Circle",
    "rtriangle": "R.Triangle",
    "etriangle": "E.Triangle",
    "rhombus":   "Rhombus",
    "fill":      "Fill",
    "eraser":    "Eraser",
    "text":      "Text",
}

SIZES = [2, 5, 10]
SIZE_LABELS = ["S", "M", "L"]
SIZE_PX = ["2px", "5px", "10px"]

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Paint Studio")

canvas = pygame.Surface((CANVAS_W, CANVAS_H))
canvas.fill(WHITE)

font_sm = pygame.font.SysFont("lucidaconsole", 12)
font_md = pygame.font.SysFont("lucidaconsole", 13, bold=True)
font_text_tool = pygame.font.SysFont("georgia", 22)
font_title = pygame.font.SysFont("lucidaconsole", 14, bold=True)

active_tool = "pencil"
active_color = BLACK
active_size_idx = 0

drawing = False
start_pos = None
prev_pos = None

text_mode = False
text_pos = None
text_buffer = ""

preview_canvas = None


def canvas_offset():
    return TOOLBAR_W, 0


def to_canvas_pos(p):
    return p[0] - TOOLBAR_W, p[1]


def get_tool_rect(idx):
    return pygame.Rect(10, 52 + idx * 32, TOOLBAR_W - 20, 28)


def get_size_rect(idx):
    base_y = 52 + len(TOOLS) * 32 + 30
    return pygame.Rect(10 + idx * 50, base_y, 44, 28)


def get_color_rect(idx):
    base_y = 52 + len(TOOLS) * 32 + 30 + 40 + 22
    return pygame.Rect(10 + (idx % 4) * 38, base_y + (idx // 4) * 38, 30, 30)


def draw_toolbar(mouse_pos):
    pygame.draw.rect(screen, PANEL, (0, 0, TOOLBAR_W, SCREEN_H))
    pygame.draw.line(screen, BORDER, (TOOLBAR_W - 1, 0), (TOOLBAR_W - 1, SCREEN_H), 2)

    title = font_title.render("PAINT STUDIO", True, BTN_ACTIVE)
    screen.blit(title, (10, 14))
    pygame.draw.line(screen, BORDER, (10, 36), (TOOLBAR_W - 10, 36), 1)

    section = font_sm.render("TOOLS", True, DIM)
    screen.blit(section, (10, 40))

    for i, tool in enumerate(TOOLS):
        r = get_tool_rect(i)
        is_active = tool == active_tool
        is_hover = r.collidepoint(mouse_pos)
        if is_active:
            color = BTN_ACTIVE
        elif is_hover:
            color = BTN_HOVER
        else:
            color = BTN
        pygame.draw.rect(screen, color, r, border_radius=5)
        if is_active:
            pygame.draw.rect(screen, (120, 230, 150), r, 1, border_radius=5)
        lbl = font_sm.render(TOOL_LABELS[tool], True, WHITE if is_active else TEXT_CLR)
        screen.blit(lbl, (r.x + 7, r.y + 8))

    base_y = 52 + len(TOOLS) * 32
    sep = font_sm.render("BRUSH SIZE", True, DIM)
    screen.blit(sep, (10, base_y + 10))

    for i in range(3):
        r = get_size_rect(i)
        is_active = i == active_size_idx
        is_hover = r.collidepoint(mouse_pos)
        if is_active:
            c = BTN_ACTIVE
        elif is_hover:
            c = BTN_HOVER
        else:
            c = BTN
        pygame.draw.rect(screen, c, r, border_radius=5)
        if is_active:
            pygame.draw.rect(screen, (120, 230, 150), r, 1, border_radius=5)
        lbl = font_md.render(SIZE_LABELS[i], True, WHITE)
        sub = font_sm.render(SIZE_PX[i], True, (150, 200, 160) if is_active else DIM)
        screen.blit(lbl, (r.x + 8, r.y + 3))
        screen.blit(sub, (r.x + 3, r.y + 16))

    base_y2 = base_y + 72
    sep2 = font_sm.render("COLORS", True, DIM)
    screen.blit(sep2, (10, base_y2))

    for i, c in enumerate(COLORS):
        r = get_color_rect(i)
        pygame.draw.rect(screen, c, r, border_radius=4)
        if c == active_color:
            pygame.draw.rect(screen, BTN_ACTIVE, r.inflate(4, 4), 2, border_radius=5)
        elif r.collidepoint(mouse_pos):
            pygame.draw.rect(screen, WHITE, r, 1, border_radius=4)

    preview_y = base_y2 + (len(COLORS) // 4) * 38 + 14
    pygame.draw.rect(screen, active_color, (10, preview_y, TOOLBAR_W - 20, 18), border_radius=3)
    pygame.draw.rect(screen, BORDER, (10, preview_y, TOOLBAR_W - 20, 18), 1, border_radius=3)

    hint1 = font_sm.render("Ctrl+S  save", True, DIM)
    hint2 = font_sm.render("1/2/3   size", True, DIM)
    screen.blit(hint1, (10, SCREEN_H - 38))
    screen.blit(hint2, (10, SCREEN_H - 22))


def render_shape(surface, tool, start, end, color, size):
    if tool == "line":
        draw_line(surface, start, end, color, size)
    elif tool == "rect":
        draw_rectangle(surface, start, end, color, size)
    elif tool == "square":
        draw_square(surface, start, end, color, size)
    elif tool == "circle":
        draw_circle(surface, start, end, color, size)
    elif tool == "rtriangle":
        draw_right_triangle(surface, start, end, color, size)
    elif tool == "etriangle":
        draw_equilateral_triangle(surface, start, end, color, size)
    elif tool == "rhombus":
        draw_rhombus(surface, start, end, color, size)


clock = pygame.time.Clock()

while True:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                active_size_idx = 0
            elif event.key == pygame.K_2:
                active_size_idx = 1
            elif event.key == pygame.K_3:
                active_size_idx = 2

            if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                pygame.image.save(canvas, f"canvas_{ts}.png")

            if text_mode:
                if event.key == pygame.K_RETURN:
                    rendered = font_text_tool.render(text_buffer, True, active_color)
                    canvas.blit(rendered, text_pos)
                    text_mode = False
                    text_buffer = ""
                    text_pos = None
                elif event.key == pygame.K_ESCAPE:
                    text_mode = False
                    text_buffer = ""
                    text_pos = None
                elif event.key == pygame.K_BACKSPACE:
                    text_buffer = text_buffer[:-1]
                else:
                    if event.unicode and event.unicode.isprintable():
                        text_buffer += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            if mx < TOOLBAR_W:
                for i, tool in enumerate(TOOLS):
                    if get_tool_rect(i).collidepoint(mx, my):
                        active_tool = tool
                        text_mode = False
                        text_buffer = ""
                for i in range(3):
                    if get_size_rect(i).collidepoint(mx, my):
                        active_size_idx = i
                for i, c in enumerate(COLORS):
                    if get_color_rect(i).collidepoint(mx, my):
                        active_color = c
            else:
                cp = to_canvas_pos((mx, my))
                if active_tool == "text":
                    text_mode = True
                    text_pos = cp
                    text_buffer = ""
                elif active_tool == "fill":
                    flood_fill(canvas, cp, active_color)
                else:
                    drawing = True
                    start_pos = cp
                    prev_pos = cp
                    preview_canvas = canvas.copy()

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if drawing:
                cp = to_canvas_pos(event.pos)
                size = SIZES[active_size_idx]
                if active_tool == "pencil":
                    draw_pencil(canvas, prev_pos, cp, active_color, size)
                elif active_tool == "eraser":
                    draw_pencil(canvas, prev_pos, cp, WHITE, size * 4)
                else:
                    render_shape(canvas, active_tool, start_pos, cp, active_color, size)
                drawing = False
                start_pos = None
                prev_pos = None
                preview_canvas = None

        if event.type == pygame.MOUSEMOTION:
            if drawing:
                cp = to_canvas_pos(event.pos)
                size = SIZES[active_size_idx]
                if active_tool == "pencil":
                    draw_pencil(canvas, prev_pos, cp, active_color, size)
                    prev_pos = cp
                elif active_tool == "eraser":
                    draw_pencil(canvas, prev_pos, cp, WHITE, size * 4)
                    prev_pos = cp

    screen.fill(BG)
    draw_toolbar(mouse_pos)

    display_canvas = canvas.copy()

    if drawing and active_tool not in ("pencil", "eraser") and preview_canvas:
        display_canvas = preview_canvas.copy()
        cp = to_canvas_pos(mouse_pos)
        size = SIZES[active_size_idx]
        render_shape(display_canvas, active_tool, start_pos, cp, active_color, size)

    if text_mode and text_pos:
        preview = font_text_tool.render(text_buffer + "|", True, active_color)
        display_canvas.blit(preview, text_pos)

    ox, oy = canvas_offset()
    screen.blit(display_canvas, (ox, oy))

    pygame.display.flip()
    clock.tick(60)
