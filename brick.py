import pygame
import os

class Brick(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, x, y, order):
        super().__init__()

        self.order = order
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen_centerx = screen_width / 2
        self.screen_centery = screen_height / 2
        base_dir = os.path.dirname(__file__)
        if self.order < 10:
            img_path = os.path.join(base_dir, "images", "bricks", "brick_diorite.png")
            self.image = pygame.image.load(img_path).convert_alpha()
        if self.order >= 10:
            img_path = os.path.join(base_dir, "images", "bricks", "brick_dark.png")
            self.image = pygame.image.load(img_path).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y