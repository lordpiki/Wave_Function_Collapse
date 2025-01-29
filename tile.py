import pygame
RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

@staticmethod
def opposite(direction):
    if direction == RIGHT:
        return LEFT
    elif direction == DOWN:
        return UP
    elif direction == LEFT:
        return RIGHT
    elif direction == UP:
        return DOWN
    
@staticmethod
def rotate_image(mat):
    """Rotate a 3x3 image clockwise the specified number of times."""
    n = len(mat)

    mat=mat.copy()
    
    # Reverse Columns
    for i in range(n // 2):
        for j in range(n):
            mat[i][j], mat[n - i - 1][j] = mat[n - i - 1][j], mat[i][j]
            
    # Perform Transpose
    for i in range(n):
        for j in range(i + 1, n):
            mat[i][j], mat[j][i] = mat[j][i], mat[i][j]
    return mat


class Tile (object):
    def __init__(self, img):
        self.img = img
        # list of possible neighbors, in order of right, down, left, up
        # each element is a list of indexes, where the indexes represent the images of possible neighbors
        self.possible_neighbors = [[], [], [], []]

    def get_possible_neighbors(self, direction):
        return self.possible_neighbors[direction]
    

    def calculate_possible_neighbors(self, tiles):
        # iterate through all the tiles
        for i, tile in enumerate(tiles):
            # check if the tile can be a neighbor in any direction
            for direction in range(4):
                if self.can_be_neighbor(tile, direction):
                    self.possible_neighbors[direction].append(i)



    def can_be_neighbor(self, other, direction):
        # Convert images to list of 3x3 of RGB values
        imageA = [[self.img.get_at((x, y))[:3] for x in range(3)] for y in range(3)]
        imageB = [[other.img.get_at((x, y))[:3] for x in range(3)] for y in range(3)]

        # Rotate the images based on direction
        if direction == RIGHT:
            pass  # No rotation needed for RIGHT
        elif direction == DOWN:
            # Rotate imageA clockwise once
            imageA = rotate_image(imageA)
            imageA = rotate_image(imageA)
            imageA = rotate_image(imageA)
            imageB = rotate_image(imageB)
            imageB = rotate_image(imageB)
            imageB = rotate_image(imageB)
            # imageB = rotate_image(imageB)
            # imageB = rotate_image(imageB)
        elif direction == LEFT:
            # Rotate imageA 180 degrees
            imageA = rotate_image(imageA)
            imageA = rotate_image(imageA)
            imageB = rotate_image(imageB)
            imageB = rotate_image(imageB)
        elif direction == UP:
            # Rotate imageA counterclockwise (3 clockwise rotations)
            imageA = rotate_image(imageA)
            imageB = rotate_image(imageB)


        # Check if the right column of the left tile matches the left column of the right tile
        for y in range(3):
            if imageA[y][2] != imageB[y][0]:
                return False
        return True
    

a = [[(255, 255, 255), (255, 255, 255), (255, 255, 255)],
      [(255, 255, 255), (0, 0, 0), (0, 0, 0)],
      [(255, 255, 255), (0, 0, 0), (237, 28, 36)]]
print(rotate_image(a))