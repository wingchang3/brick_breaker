import pygame
from paddle import Paddle
from ball import Ball
from font_block import Font_block
from brick import Brick

class Game:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen_center = (screen_width / 2, screen_height / 2)
        self.font_36 = pygame.font.Font(None, 36)
        self.font_144 = pygame.font.Font(None, 144)
        self.level = 0
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        self.all_sprites = pygame.sprite.Group()
        self.paddle = Paddle(self.screen_width, self.screen_height)
        self.font_block = Font_block(self.screen_width, self.screen_height)
        self.ball = Ball(self.screen_width, self.screen_height)
        self.lives = 3
        self.scores = 0
        self.blit_or_renew_font_lives()
        self.blit_or_renew_font_scores()
        self.blit_or_renew_font_the_end()
        self.ready_reset_game()
    
    def spawn_brick(self):
        #self.brick_order_list = [object, able_collision]
        self.brick_order_list = []
        self.brick_locate_list = []
        for i in range(10):
            self.brick_locate_list.append([75 + (i * 112.5), 75])
            self.brick_order_list.append([Brick(self.screen_width, self.screen_height, 75 + (i * 112.5), 75, i), True])
            self.all_sprites.add(self.brick_order_list[i][0])
        for i in range(10, 20):
            self.brick_locate_list.append([75 + ((i - 10) * 112.5), 150])
            self.brick_order_list.append([Brick(self.screen_width, self.screen_height, (75 + (i - 10) * 112.5), 150, i), True])
            self.all_sprites.add(self.brick_order_list[i][0])
    
    def ready_reset_game(self):
        self.all_sprites.add(self.font_block)
    
    def reset_game(self):
        if self.level == 0:
            self.hide_item(self.font_block)
            self.ball.locate()
            self.ball.move()
            self.all_sprites.add(self.ball, self.paddle)
            self.spawn_brick()
            self.lives = 3
            self.brick_amount = 20
            self.blit_or_renew_font_lives()
            self.level = 1

    def hide_item(self, hide_item):
        self.all_sprites.remove(hide_item)

    def blit_or_renew_font_lives(self):
        self.text_lives = self.font_36.render(f"lives =  {self.lives}", True, (255, 0 ,0))
        self.text_rect_lives = self.text_lives.get_rect(topright=(self.screen_width - 10, 10))
    
    def blit_or_renew_font_scores(self):
        self.text_scores = self.font_36.render(f"scores =  {self.scores}", True, (255, 0 ,0))
        self.text_rect_scores = self.text_scores.get_rect(topleft=(0 + 10, 10))
    
    def blit_or_renew_font_the_end(self):
        self.text_the_end = self.font_144.render(f"Congratulations!!", True, (0, 255 ,0))
        self.text_rect_the_end = self.text_the_end.get_rect(center=(self.screen_center))

    def if_ball_paddle_collision(self):
        if pygame.sprite.collide_rect(self.paddle, self.ball):
            self.ball.paddle_collision(self.paddle.rect.center)
            self.paddle_v = self.mouse_x - self.mouse_x_before
            self.ball.friction_with_paddle(self.paddle_v)
    
    def if_ball_brick_collision(self):
        for i in range(20):
            if self.level == 1:
                if pygame.sprite.collide_rect(self.ball, self.brick_order_list[i][0]) and self.brick_order_list[i][1] == True:
                    self.all_sprites.remove(self.brick_order_list[i][0])
                    self.brick_order_list[i][1] = False
                    self.brick_amount -= 1
                    self.ball.brick_collision(self.brick_locate_list[i])
                    if i < 10:
                        self.scores += 20
                        self.ball.speed += 1
                    else:
                        self.scores += 10
                    self.blit_or_renew_font_scores()
    
    def if_the_end(self):
        if self.brick_amount == 0 and self.level == 1:
            self.level = 2
            self.hide_item(self.paddle)
            self.hide_item(self.ball)
    
    def if_ball_side_collision(self):
        if self.ball.rect.left < 0:
            self.ball.vectorx *= -1
            self.scores -= 1
            self.blit_or_renew_font_scores()
        if self.ball.rect.right > self.screen_width:
            self.ball.vectorx *= -1
            self.scores -= 1
            self.blit_or_renew_font_scores()
        if self.ball.rect.top < 0:
            self.ball.vectory *= -1
            self.scores -= 1
            self.blit_or_renew_font_scores()

    def if_die(self):
        if self.ball.rect.top > self.screen_height:
            self.lives -= 1
            self.ball.locate()
            self.ball_speed = self.ball.speed
            self.level -= 0.5
            self.ball.stop()
            self.ball.reset()
            self.blit_or_renew_font_lives()
            if self.lives == 0:
                self.scores //= 2
                self.blit_or_renew_font_scores()
                self.restart()
    
    def restart(self):
        for i in range(20):
            self.all_sprites.remove(self.brick_order_list[i][0])
        self.ball.stop()
        self.hide_item(self.ball)
        self.hide_item(self.paddle)
        self.brick_locate_list.clear()
        self.brick_order_list.clear()
        self.scores = 0
        self.level = 0
        self.ready_reset_game()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.MOUSEBUTTONDOWN:
                # 左鍵  
                if self.font_block.rect.collidepoint(self.mouse_x, self.mouse_y):
                    self.reset_game()
                if self.level == 0.5:
                    self.ball.speed = self.ball_speed
                    self.level = 1

        return False
            
    def update(self):
        self.mouse_x_before = self.mouse_x
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        
        self.paddle.follow_mousex(self.mouse_x)
        if self.level == 1:
            self.if_ball_paddle_collision()
            self.if_ball_brick_collision()
            self.if_ball_side_collision()
            self.if_die()
            self.if_the_end()
        self.ball.update()
    
    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.all_sprites.draw(screen)
        screen.blit(self.text_lives, self.text_rect_lives)
        screen.blit(self.text_scores, self.text_rect_scores)
        if self.level == 2:
            screen.blit(self.text_the_end, self.text_rect_the_end)
        pygame.display.flip()