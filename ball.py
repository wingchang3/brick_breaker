import pygame
import random
import math

class Ball(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.RED = (255,255,255)
        self.brick_width = 75
        self.brick_height = 22.5
        self.paddle_width = 120
        self.paddle_height = 15
        self.size = 7.5
        self.reset()
        self.move()
        
        self.screen_centerx = screen_width / 2
        self.screen_centery = screen_height / 2
        self.image = pygame.Surface((self.size * 2, self.size * 2),pygame.SRCALPHA)
        pygame.draw.circle(self.image,self.RED,(self.size,self.size),self.size)
        self.rect = self.image.get_rect()
        self.locate()
    
    def locate(self):
        self.rect.center = (self.screen_centerx, self.screen_centery)

    def paddle_collision(self, paddle_location):
        self.paddle_x, self.paddle_y = paddle_location
        self.d_paddle_x = self.rect.centerx - self.paddle_x
        self.d_paddle_y = self.rect.centery - self.paddle_y
        self.overlap_paddle_x = (self.paddle_width / 2) + self.size - abs(self.d_paddle_x)
        self.overlap_paddle_y = (self.paddle_height / 2) + self.size - abs(self.d_paddle_y)
        if self.overlap_paddle_x > self.overlap_paddle_y:
            self.rect.y += self.d_paddle_y
            self.vectory *= -1
        else:
            self.rect.x += self.d_paddle_x
            self.vectorx *= -1
    
    def brick_collision(self, brick_location):
        self.brick_x, self.brick_y = brick_location
        self.brick_center_x = self.brick_x + (self.brick_width / 2)
        self.brick_center_y = self.brick_y + (self.brick_height / 2)
        self.d_brick_x = self.rect.centerx - self.brick_center_x
        self.d_brick_y = self.rect.centery - self.brick_center_y
        self.overlap_brick_x = (self.brick_width / 2) + self.size - abs(self.d_brick_x)
        self.overlap_brick_y = (self.brick_height / 2) + self.size - abs(self.d_brick_y)
        if self.overlap_brick_x > self.overlap_brick_y:
            self.vectory *= -1
        else:
            self.vectorx *= -1
    
    def friction_with_paddle(self, paddle_v):
        self.vectorx += paddle_v / 2
        self.vectorx = self.vectorx / (math.pow(math.pow(self.vectorx, 2) + math.pow(self.vectory, 2), 0.5))
        self.vectory = self.vectory / (math.pow(math.pow(self.vectorx, 2) + math.pow(self.vectory, 2), 0.5))

    def reset(self):
        self.angle = random.randrange(225, 316) % 360
        self.target = self.angle * (-1)
        self.radians = math.radians(self.target)
        self.vectorx = math.cos(self.radians)
        self.vectory = math.sin(self.radians)

    def stop(self):
        self.speed = 0
    
    def move(self):
        self.speed = 10

    def update(self):
        self.rect.x += self.vectorx * self.speed
        self.rect.y += self.vectory * self.speed
        