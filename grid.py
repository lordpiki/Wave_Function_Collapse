import render as renderer
from tile import *
import random
# random.seed(1)
MAX_ENTROPY = 81

class Cell(object):
    
    def __init__(self, x, y, options):
        self.x = x
        self.y = y
        self.collapsed = False
        self.options = options
        self.checked = False

    def calculate_entropy(self):
        return len(self.options)
    

class Grid(object):
    def __init__(self):
        self.tiles = self.load_tiles("ColoredCity.png")
        # set an empty 20x20 grid of tiles
        self.size = 20
        self.grid = [[Cell(x, y, []) for x in range(self.size)] for y in range(self.size)]

    def load_tiles(self, path):
        images = renderer.load_image(path)
        tiles = [Tile(img) for img in images]
        # go over all the tiles, if 2 tiles have the same image, then increase the frequency of the first tile and remove the second tile
        for tile in tiles:
            for other_tile in tiles:
                if renderer.identical(tile.img, other_tile.img) and tile != other_tile:
                    tile.frequency += 1
                    tiles.remove(other_tile)
        for index, tile in enumerate(tiles):
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
        
    
    def test_tile_neighbors(self, tile_index):
        tile = self.tiles[tile_index]
        # make the tile the last tile in the grid
        self.grid[19][19].collapsed = True
        self.grid[19][19].options = [tile_index]
        # iterate through all the possible neighbors
        # set the grid of all the neighbors to the possible neighbors of the tile
        # tile_neighbors = tile.get_possible_neighbors(UP)
        # tile_neighbors = tile.get_possible_neighbors(DOWN)
        tile_neighbors = tile.get_possible_neighbors(RIGHT)
        # tile_neighbors = tile.get_possible_neighbors(LEFT)
        
        for y in range(self.size):
            for x in range(self.size):
                if x + y * self.size in tile_neighbors:
                    self.grid[y][x].options = [x + y * self.size]
                    self.grid[y][x].collapsed = True
                
    def reset_grid(self):
        self.grid = [[Cell(x, y, [index for index in range(len(self.tiles))]) for x in range(self.size)] for y in range(self.size)]


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
                    cell.options = [cell.options[0]]
                    self.reduce_entropy(cell)
                if entropy == 0:
                    print("Error: Entropy is 0")
                    # reset the grid and try again
                    self.reset_grid()
                    self.render()
                    return
                if entropy < lowest_entropy:
                    lowest_entropy = entropy
                    lowest_entropy_cells = [cell]
                elif entropy == lowest_entropy:
                    lowest_entropy_cells.append(cell)
        
        # Collapse a random cell from the list of cells with the lowest entropy
        if len(lowest_entropy_cells) > 0:
            picked_cell = random.choice(lowest_entropy_cells)
            picked_cell.collapsed = True
            tiles_frequencies = [self.tiles[index].frequency for index in picked_cell.options]
            # Give the tiles with the highest frequency a higher chance of being picked
            picked_cell.options = [random.choices(picked_cell.options, weights=tiles_frequencies)[0]]
            # picked_cell.options = [random.choice(picked_cell.options)]


            # Update the neighbors of the picked cell
            # self.update_neighbors(picked_cell)
            self.reduce_entropy(picked_cell)

    def update_neighbors(self, cell):
        for direction in range(4):
            neighbor = self.get_neighbor(cell.x, cell.y, direction)
            if neighbor is not None and neighbor.collapsed == False:
                # remove the options that are not possible
                neighbor.options = [option for option in neighbor.options if option in self.tiles[cell.options[0]].get_possible_neighbors(direction)]

    def reduce_entropy(self, cell):
        # check if the is collapsed or if the cell has already been checked
        if cell.checked:
            return
        cell.checked = True
        

        # reduce the entropy of the neighbors recursively
        for direction in range(4):
            # get the all the options of the neighbor's cell based on all the possible tiles of this cell
            total_options = []
            for tile_index in cell.options:
                total_options += self.tiles[tile_index].possible_neighbors[direction]
                
            neighbor = self.get_neighbor(cell.x, cell.y, direction)
            if neighbor is not None:
                if not neighbor.collapsed:
                    # remove the options that are not possible
                    neighbor.options = [option for option in neighbor.options if option in total_options]

                # neighbor.checked = True
                self.reduce_entropy(neighbor)
        

    def get_neighbor(self, x, y, direction) -> Cell:
        if direction == 0:
            if x + 1 < self.size:
                return self.grid[y][x + 1]
        elif direction == 1:
            if y + 1 < self.size:
                return self.grid[y + 1][x]
        elif direction == 2:
            if x - 1 >= 0:
                return self.grid[y][x - 1]
        elif direction == 3:
            if y - 1 >= 0:
                return self.grid[y - 1][x]
        return None



        

if __name__ == "__main__":
    grid = Grid()   
    # grid.test_tile_neighbors(10)
    grid.showcase_base_img()    
    # grid.reset_grid()

    # grid.wfc()
    grid.render()   

