import pygame
import sys

def render(grid: list, scale: int = 20):
    pygame.init()
    screen = pygame.display.set_mode((len(grid[0]) * scale, len(grid) * scale))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        for y, row in enumerate(grid):
            for x, color in enumerate(row):
                pygame.draw.rect(screen, color, (x * scale, y * scale, scale, scale))
                # draw grid lines
                pygame.draw.rect(screen, (0,0,0), (x * scale, y * scale, scale, scale), 1)
                
        pygame.display.update()
        # pygame.time.delay(1000)

