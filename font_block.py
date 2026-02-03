import pygame
import os

class Font_block(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen_centerx = screen_width / 2
        self.screen_centery = screen_height / 2

        base_dir = os.path.dirname(__file__)
        img_path = os.path.join(base_dir, "images", "font_block", "play.png")
        self.image = pygame.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.center = (self.screen_centerx, self.screen_centery)