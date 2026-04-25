import pygame
from collections import deque


def draw_pencil(surface, start, end, color, size):
    pygame.draw.line(surface, color, start, end, size)


def draw_line(surface, start, end, color, size):
    pygame.draw.line(surface, color, start, end, size)


def draw_rectangle(surface, start, end, color, size):
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    w = abs(end[0] - start[0])
    h = abs(end[1] - start[1])
    pygame.draw.rect(surface, color, (x, y, w, h), size)


def draw_square(surface, start, end, color, size):
    side = min(abs(end[0] - start[0]), abs(end[1] - start[1]))
    x = start[0]
    y = start[1]
    if end[0] < start[0]:
        x = start[0] - side
    if end[1] < start[1]:
        y = start[1] - side
    pygame.draw.rect(surface, color, (x, y, side, side), size)


def draw_circle(surface, start, end, color, size):
    cx = (start[0] + end[0]) // 2
    cy = (start[1] + end[1]) // 2
    r = int(((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5 // 2)
    if r > 0:
        pygame.draw.circle(surface, color, (cx, cy), r, size)


def draw_right_triangle(surface, start, end, color, size):
    p1 = start
    p2 = (start[0], end[1])
    p3 = end
    pygame.draw.polygon(surface, color, [p1, p2, p3], size)


def draw_equilateral_triangle(surface, start, end, color, size):
    base = abs(end[0] - start[0])
    height = int(base * (3 ** 0.5) / 2)
    x = min(start[0], end[0])
    y = start[1]
    p1 = (x, y + height)
    p2 = (x + base, y + height)
    p3 = (x + base // 2, y)
    pygame.draw.polygon(surface, color, [p1, p2, p3], size)


def draw_rhombus(surface, start, end, color, size):
    cx = (start[0] + end[0]) // 2
    cy = (start[1] + end[1]) // 2
    p1 = (cx, start[1])
    p2 = (end[0], cy)
    p3 = (cx, end[1])
    p4 = (start[0], cy)
    pygame.draw.polygon(surface, color, [p1, p2, p3, p4], size)


def flood_fill(surface, pos, fill_color):
    target_color = surface.get_at(pos)[:3]
    fill_rgb = fill_color[:3] if len(fill_color) == 4 else fill_color
    if target_color == fill_rgb:
        return
    width, height = surface.get_size()
    queue = deque()
    queue.append(pos)
    visited = set()
    visited.add(pos)
    while queue:
        x, y = queue.popleft()
        surface.set_at((x, y), fill_color)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
                if surface.get_at((nx, ny))[:3] == target_color:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
