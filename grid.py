import render as renderer
from tile import *
import random

MAX_ENTROPY = 81

class Cell(object):
    
    def __init__(self, x, y, options):
        self.x = x
        self.y = y
        self.collapsed = False
        self.options = options

    def calculate_entropy(self):
        return len(self.options)
    

class Grid(object):
    def __init__(self):
        self.tiles = self.load_tiles("City.png")
        # set an empty 20x20 grid of tiles
        self.grid = [[Cell(x, y, []) for x in range(20)] for y in range(20)]
        self.size = 20

    def load_tiles(self, path):
        images = renderer.load_image(path)
        tiles = [Tile(img) for img in images]
        for tile in tiles:
            tile.calculate_possible_neighbors(tiles)
        return tiles
    
    def render(self):
        renderer.render(self)
    
    def showcase_base_img(self):
        # start assigning images to the tiles, if there are no more images, make it a blank img
        for y in range(self.size):
            for x in range(self.size):
                # check if the x,y index is out of bounds
                if x + y * self.size >= len(self.tiles):
                    self.grid[y][x].collapsed = False
                else:
                    self.grid[y][x].collapsed = True
                    self.grid[y][x].options = [x + y * self.size]

    def reset_grid(self):
        self.grid = [[Cell(x, y, [index for index in range(len(self.tiles))]) for x in range(20)] for y in range(20)]


    def get_tiles(self):
        return self.tiles
    
    def wfc(self):
        # Make a list of all the cells with the lowest entropy
        # If on the way is a cell with entropy 1, collapse the cell
        # Pick a random cell from the list of cells with the lowest entropy and collapse it
        # Update the entropy of all the neighbors
        # Repeat until all cells are collapsed

        # Getting a list of all the cells with the lowest entropy
        lowest_entropy = MAX_ENTROPY
        lowest_entropy_cells = []
        for y in range(self.size):
            for x in range(self.size):
                cell = self.grid[y][x]
                if cell.collapsed:
                    continue
                entropy = cell.calculate_entropy()
                if entropy == 1:
                    cell.collapsed = True
                    continue
                if entropy < lowest_entropy:
                    lowest_entropy = entropy
                    lowest_entropy_cells = [cell]
                elif entropy == lowest_entropy:
                    lowest_entropy_cells.append(cell)
        
        # Collapse a random cell from the list of cells with the lowest entropy
        if len(lowest_entropy_cells) > 0:
            cell = lowest_entropy_cells[random.randint(0, len(lowest_entropy_cells) - 1)]
            cell.collapsed = True
            cell.options = [cell.options[random.randint(0, len(cell.options) - 1)]]

        # Update the entropy of all the neighbors
        # TODO: implement this


        

if __name__ == "__main__":
    grid = Grid()   
    # grid.showcase_base_img()    
    grid.reset_grid()
    grid.wfc()
    grid.render()   