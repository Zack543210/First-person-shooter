from settings import *


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wallTextures = self.loadWallTextures()
        self.skyImage = self.getTexture('images/resources/textures/sky1.png', (WIDTH, HALF_HEIGHT))
        self.skyOffset = 0
        self.bloodScreen = self.getTexture('images/resources/textures/bloodScreen.png', RES)
        self.digitSize = ZOOM * 9
        self.digitImages = [self.getTexture(f'images/resources/digits/{i}.png',[self.digitSize] * 2) for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digitImages))
        self.gameOverImage = self.getTexture('images/resources/textures/gameOver.png', RES)

    def draw(self):
        self.drawBackground()
        self.renderGameObjects()
        self.drawPlayerHealth()

    def gameOver(self):
        self.screen.blit(self.gameOverImage, (0, 0))

    def drawPlayerHealth(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digitSize, 0))
        self.screen.blit(self.digits['10'], ((i + 1) * self.digitSize, 0))

    def playerDamage(self):
        self.screen.blit(self.bloodScreen, (0, 0))

    def drawBackground(self):
        #sky
        self.skyOffset = (self.skyOffset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.skyImage, (-self.skyOffset, 0))
        self.screen.blit(self.skyImage, (-self.skyOffset + WIDTH, 0))
        #floor
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def renderGameObjects(self):
        listObjects = sorted(self.game.raycasting.objectsToRender, key=lambda t: t[0], reverse=True)
        for depth, image, pos in listObjects:
            self.screen.blit(image, pos)

    @staticmethod
    def getTexture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def loadWallTextures(self):
        return {
            1: self.getTexture('images/resources/textures/1.png'),
            2: self.getTexture('images/resources/textures/2.png'),
            3: self.getTexture('images/resources/textures/3.png'),
            4: self.getTexture('images/resources/textures/4.png'),
            5: self.getTexture('images/resources/textures/5.png')
        }