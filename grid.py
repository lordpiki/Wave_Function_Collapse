from render import *
from tile import *


images = load_image("City.png")
black_image = pygame.Surface((3, 3))
# set an empty 20x20 grid of tiles
grid = [[Tile(x, y, images[0]) for x in range(20)] for y in range(20)]
# start assigning images to the tiles, if there are no more images, make it a blank img
for y in range(len(grid)):
    for x in range(len(grid[y])):
         # if images is empty, make and use a black image
        grid[y][x].img = images.pop(0) if images else black_image
print(grid[0][2].can_be_neighbor(grid[0][2], RIGHT))
render(grid)