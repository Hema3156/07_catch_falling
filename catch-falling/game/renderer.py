"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

from game.basket import BOOST_DURATION_FRAMES, BOOST_COOLDOWN_FRAMES

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (25, 30, 45)
COLOR_BASKET = (150, 110, 70)
COLOR_BASKET_BOOST = (80, 220, 255)
COLOR_TEXT = (255, 255, 255)
COLOR_BOOST = (80, 220, 255)


def draw_scene(surface, basket, objects):
    surface.fill(COLOR_BG)
    for obj in objects:
        pygame.draw.circle(surface, obj.color, (int(obj.x), int(obj.y)), obj.radius)
    color = COLOR_BASKET_BOOST if basket.is_boosted else COLOR_BASKET
    pygame.draw.rect(surface, color, basket.get_rect(), border_radius=6)


def draw_boost_status(surface, font, basket):
    x, y, w, h = WIDTH - 220, 12, 200, 14
    if basket.is_boosted:
        draw_text(surface, font, "SPEED BOOST!", (x, y + 18), COLOR_BOOST)
        frac = basket.boosted_frames / BOOST_DURATION_FRAMES
        pygame.draw.rect(surface, (60, 70, 90), (x, y, w, h), border_radius=4)
        pygame.draw.rect(surface, COLOR_BOOST, (x, y, int(w * frac), h), border_radius=4)
    elif basket.cooldown_frames > 0:
        secs = basket.cooldown_frames / 60
        draw_text(surface, font, f"Boost ready in {secs:.0f}s", (x, y), (170, 170, 170))
    else:
        draw_text(surface, font, "SPACE: speed boost", (x, y), COLOR_TEXT)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_banner(surface, font, text):
    surf = font.render(text, True, (255, 220, 80))
    rect = surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
    surface.blit(surf, rect)