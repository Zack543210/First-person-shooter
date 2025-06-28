import pygame as pg

_ = False

miniMap = [
    [2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [2, _, _, _, _, _, 1, _, _, _, 4, _, _, _, _, 1],
    [2, _, _, 2, 3, 3, 1, _, _, _, 4, _, _, _, _, 4],
    [3, _, _, _, _, _, 1, _, _, 5, 1, 1, 1, 4, _, 4],
    [3, _, _, _, _, _, 1, _, _, _, _, _, 1, _, _, 5],
    [2, _, _, 2, 3, 3, 1, _, _, _, _, _, 1, _, _, 1],
    [1, _, _, _, _, _, _, _, 1, 1, 5, _, 5, _, _, 1],
    [1, _, 3, _, _, _, _, _, 1, _, _, _, _, _, _, 1],
    [1, 1, 2, 2, 4, 1, 1, 1, 1, 5, 5, 4, 5, 1, 1, 1]
]

class Map:
    def __init__(self, game):
        self.game = game
        self.miniMap = miniMap
        self.worldMap = {}
        self.getMap()

    def getMap(self):
        for j, row in enumerate(self.miniMap):
            for i, value in enumerate(row):
                if value:
                    self.worldMap[(i, j)] = value

    def draw(self, color):
        [pg.draw.rect(self.game.screen, color, (pos[0] * 100, pos[1] * 100, 100, 100), 2)
         for pos in self.worldMap]
        