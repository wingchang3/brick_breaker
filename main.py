import pygame
from game import Game

def main():
    pygame.init()

    SCREEN_WIDTH = 1275
    SCREEN_HEIGHT = 600

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("brick breaker")
    clock = pygame.time.Clock()
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)

    running = True
    while running:
        done = game.process_events()
        if done:
            running = False
        
        game.update()
        game.draw(screen)

        clock.tick(120)

    pygame.quit()

#cannot implement in other .py
if __name__ == "__main__":
    main()