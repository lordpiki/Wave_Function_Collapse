import pygame
RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

class Tile (object):
    def __init__(self, x, y, img):
        self.pos = (x, y)
        self.img = img
        self.entropy = 0
        # list of possible neighbors, in order of right, down, left, up
        # each element is a list of indexes, where the indexes represent the images of possible neighbors
        self.possible_neighbors = [[], [], [], []]

    
    def calculate_entropy(self):
        pass
    
    def calculate_possible_neighbors(self):
        pass

    def can_be_neighbor(self, other, direction):
        # the tiles can be neighbors if the right column if the right column of the left tile is the same as the left column of the right tile
        # rotate the images so that that the direction that is checked will always be the right coulmn of the left tiles
        # always check from the right, and rotate the images accordingly to avoid having 4 different cases
        # if the right column of the left tile is the same as the left column of the right tile, then the tiles can be neighbors
        # rotate based on direction
        
        # convert images to list of 3x3 of rgb values
        imageA = [[self.img.get_at((x, y))[:3] for x in range(3)] for y in range(3)]
        imageB = [[other.img.get_at((x, y))[:3] for x in range(3)] for y in range(3)]
        
        # rotate the images based on direction
        if direction == RIGHT:
            pass
        elif direction == DOWN:
            imageA = list(zip(*imageA[::-1]))
            imageB = list(zip(*imageB[::-1]))
        elif direction == LEFT:
            imageA = list(zip(*imageA[::-1]))[::-1]
            imageB = list(zip(*imageB[::-1]))[::-1]
        elif direction == UP:
            imageA = list(zip(*imageA))[::-1]
            imageB = list(zip(*imageB))[::-1]

        # check if the right column of the left tile is the same as the left column of the right tile
        return all(imageA[y][2] == imageB[y][0] for y in range(3))
        
