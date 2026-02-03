import pygame
import os

class Paddle(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        #subject init first
        super().__init__()
        base_dir = os.path.dirname(__file__)
        img_path = os.path.join(base_dir, "images", "paddle", "paddle_normal.png")
        self.image = pygame.image.load(img_path).convert_alpha()

        self.screen_width = screen_width
        self.screen_hight = screen_height
        self.screen_centerx = screen_width / 2
        self.screen_centery = screen_height / 2

        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen_centerx
        self.rect.bottom = screen_height - 50

    def follow_mousex(self, mouse_x):
        if not (self.rect.left < 0 or self.rect.right > self.screen_width):
            self.rect.centerx = mouse_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width