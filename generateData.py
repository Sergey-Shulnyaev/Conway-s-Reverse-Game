from PIL import Image
import numpy as np
import json
from random import random, uniform, randint

class ConwayGame:
    def __init__(self, matr=[], x_size=25, y_size=25):
        self.matr = matr
        self.id = 0
        self.x_size, self.y_size = x_size, y_size
        self.delta = 0

    def generateInitialBoard(self):
        density = uniform(1, 99)
        self.matr = np.array([[int(uniform(0, 100) < density) for j in range(self.x_size)] for i in range(self.y_size)],
                             dtype=np.int8)

    def generateStartBoard(self):
        self.generateInitialBoard()
        for i in range(5):
            self.runStep()

    def generateFinalBoard(self):
        self.delta = randint(1, 5)
        for i in range(self.delta):
            self.runStep()

    def createGame(self):
        path = "data/"
        self.generateStartBoard()
        start = self.matr.tolist()

        self.generateFinalBoard()
        final = self.matr.tolist()
        result = [self.delta]
        result.extend(start)
        result.extend(final)
        json_file = str(self.id) + ".json"
        with open(path+json_file, "w") as write_file:
            json.dump(result, write_file)
        self.id += 1

    def createGen(self, numb = 50000):
        for i in range(numb):
            self.createGame()

    def runStep(self):
        new_matr = np.zeros((self.x_size,self.y_size), dtype=np.int8)
        for y in range(self.y_size):
            for x in range(self.x_size):
                if self.isAlive((x, y)):
                    new_matr[y][x] = 1
        self.matr = new_matr

    def isAlive(self, pos):
        x, y = pos
        neighbors = self.mooreNeighborhood(pos)
        if self.matr[y][x] == 1:
            return 2 <= neighbors <= 3
        else:
            return neighbors == 3

    def mooreNeighborhood(self, pos):
        x, y = pos
        x_min, x_max = max(x-1, 0), min(x+1, self.x_size - 1)
        y_min, y_max = max(y - 1, 0), min(y + 1, self.y_size - 1)
        alive_cells = 0
        for i_x in range(x_min, x_max + 1):
            for j_y in range(y_min, y_max + 1):
                if self.matr[j_y][i_x] == 1:
                    alive_cells += 1
        if self.matr[y][x] == 1:
            alive_cells -= 1

        return alive_cells

    def cellGameToImage(self, name="new"):
        matr_image = np.array([[(j*255, j*255, j*255) for j in i] for i in self.matr], dtype=np.uint8)
        new_image = Image.fromarray(matr_image)
        new_image.save(name + '.png')


game = ConwayGame()
game.createGen()