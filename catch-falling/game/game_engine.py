"""
GameEngine: owns the basket and all falling objects.
"""

import random
import pygame

from game.basket import Basket
from game.falling_object import FallingObject
from game.collision import is_caught
from game.renderer import WIDTH, HEIGHT

MAX_MISSES = 5

# Spawning (Task 3)
SPAWN_MIN_FRAMES = 25
SPAWN_MAX_FRAMES = 80
MAX_OBJECTS = 8          # cap on simultaneous objects
MIN_SPAWN_GAP = 70       # min horizontal distance from the previous spawn
SPAWN_MARGIN = 14        # = object radius, keeps objects inside the screen


class GameEngine:
    def __init__(self):
        self.basket = Basket(x=WIDTH / 2, y=HEIGHT - 30)
        self.objects = []
        self.frames_until_spawn = 0
        self.last_spawn_x = None
        self.score = 0
        self.misses = 0
        self.game_over = False

    def _pick_spawn_x(self):
        lo, hi = SPAWN_MARGIN, WIDTH - SPAWN_MARGIN
        x = random.randint(lo, hi)
        for _ in range(20):
            if self.last_spawn_x is None or abs(x - self.last_spawn_x) >= MIN_SPAWN_GAP:
                break
            x = random.randint(lo, hi)
        return x

    def _spawn_object(self):
        if len(self.objects) >= MAX_OBJECTS:
            return False
        x = self._pick_spawn_x()
        self.last_spawn_x = x
        speed = random.uniform(2.5, 4.0)
        self.objects.append(FallingObject(x=x, y=-14, speed=speed))
        return True

    def handle_input(self, keys_pressed):
        if self.game_over:
            return
        direction = 0
        if keys_pressed[pygame.K_LEFT]:
            direction -= 1
        if keys_pressed[pygame.K_RIGHT]:
            direction += 1
        self.basket.move(direction, WIDTH)

    def handle_keydown(self, key):
        if self.game_over and key == pygame.K_r:
            self.__init__()
        elif not self.game_over and key == pygame.K_SPACE:
            self.basket.activate_boost()

    def update(self):
        if self.game_over:
            return

        self.basket.update()

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self._spawn_object()
            self.frames_until_spawn = random.randint(SPAWN_MIN_FRAMES, SPAWN_MAX_FRAMES)

        for obj in self.objects:
            obj.update()

        # Build a new list instead of removing while iterating (Task 1 fix):
        # every object is checked exactly once per frame.
        basket_rect = self.basket.get_rect()
        remaining = []
        for obj in self.objects:
            if is_caught(basket_rect, obj):
                self.score += 1
            elif obj.is_past_bottom(HEIGHT):
                self.misses += 1
            else:
                remaining.append(obj)
        self.objects = remaining

        if self.misses >= MAX_MISSES:
            self.game_over = True

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.basket, self.objects)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Misses: {self.misses}/{MAX_MISSES}", (10, 36))
        renderer.draw_boost_status(surface, font, self.basket)

        if self.game_over:
            renderer.draw_banner(surface, font, f"Game Over! Final score: {self.score}. Press R to restart.")