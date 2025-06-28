#51:05
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from objectRenderer import *
from spriteObject import *
from objectHandler import *
from weapon import Weapon #Increase the imports if neccesary
from sound import Sound
from pathfinding import PathFinding


class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.deltaTime = 1
        self.globalTrigger = False
        self.globalEvent = pg.USEREVENT + 0
        pg.time.set_timer(self.globalEvent, 45)
        self.newGame()

    def newGame(self):
        self.map = Map(self)
        self.player = Player(self)
        self.objectRenderer = ObjectRenderer(self)
        self.raycasting = Raycasting(self)
        self.objectHandler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.objectHandler.update()
        self.weapon.update()
        pg.display.flip()
        self.deltaTime = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.objectRenderer.draw()
        self.weapon.draw()
        # self.screen.fill('black')
        # self.map.draw('blue')
        # self.player.draw()

    def checkEvents(self):
        self.globalTrigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.globalEvent:
                self.globalTrigger = True
            self.player.singleFireEvent(event)

    def run(self):
        while True:
            self.checkEvents()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Game()
    game.run()