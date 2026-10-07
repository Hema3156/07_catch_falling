"""
Basket: the player-controlled catcher at the bottom of the screen.
"""

import pygame

BOOST_DURATION_FRAMES = 180   # 3 seconds at 60 FPS
BOOST_COOLDOWN_FRAMES = 300   # 5 seconds before it can be used again


class Basket:
    def __init__(self, x, y, width=90, height=24, speed=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.normal_speed = speed
        self.boost_speed = speed * 2
        self.speed = speed
        self.boosted_frames = 0
        self.cooldown_frames = 0

    @property
    def is_boosted(self):
        return self.boosted_frames > 0

    def activate_boost(self):
        if not self.is_boosted and self.cooldown_frames == 0:
            self.boosted_frames = BOOST_DURATION_FRAMES
            self.speed = self.boost_speed

    def update(self):
        """Call once per frame: counts the boost/cooldown timers down."""
        if self.boosted_frames > 0:
            self.boosted_frames -= 1
            if self.boosted_frames == 0:
                self.speed = self.normal_speed          # back to normal
                self.cooldown_frames = BOOST_COOLDOWN_FRAMES
        elif self.cooldown_frames > 0:
            self.cooldown_frames -= 1

    def move(self, direction, screen_width):
        """direction: -1 (left), 0, +1 (right). Keeps the basket fully on screen."""
        self.x += direction * self.speed
        half = self.width / 2
        self.x = max(half, min(screen_width - half, self.x))

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2), int(self.y - self.height / 2),
            self.width, self.height,
        )