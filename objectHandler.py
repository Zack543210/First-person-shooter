from spriteObject import *
from npc import Soldier, Cacodemon

class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.spriteList = []
        self.npcList = []
        self.npcSpritePatah = 'images/resources/sprites/npc'
        self.staticSpritePath = 'images/resources/sprites/staticSprites/'
        self.animSpritePath = 'images/resources/sprites/animatedSprites/'
        addSprite = self.addSprite
        addNpc = self.addNpc
        self.npcPositions = {}

        #sprite map
        addSprite(SpriteObject(game))#Inbase Candle
        addSprite(SpriteObject(game, pos=(5.8, 1.15)))#Base candle
        addSprite(SpriteObject(game, pos=(9.8, 2.85)))#Opp red light candle
        addSprite(SpriteObject(game, pos=(9.8, 1.15)))#Beside top candle candle
        addSprite(SpriteObject(game, pos=(13.15, 4.15)))#Corner of walls to boss
        addSprite(SpriteObject(game, pos=(11.15, 2)))#Boss candle
        addSprite(AnimatedSprite(game, pos=(5.9, 3.1)))#Inbase green light
        addSprite(AnimatedSprite(game, pos=(1.1, 7.9)))#Bottom left corner of map
        addSprite(AnimatedSprite(game, pos=(7.1, 1.1)))#Opp base green light
        addSprite(AnimatedSprite(game, pos=(5, 6.1))) #Base middle green light
        addSprite(AnimatedSprite(game, pos=(9.1, 7.5)))#Bottom, middle of map green light
        addSprite(AnimatedSprite(game, pos=(7.9, 7.9)))#Closebase green light
        addSprite(AnimatedSprite(game, pos=(11.9, 4.1)))#Opposite corner of walls to boss green light
        addSprite(AnimatedSprite(game, self.animSpritePath+'redlight/0.png', (7.1, 5.9)))#Closebase red light
        addSprite(AnimatedSprite(game, self.animSpritePath+'redlight/0.png', (10.9, 5.9)))#Leading to boss red light
        addSprite(AnimatedSprite(game, self.animSpritePath+'redlight/0.png', (14.9, 7.9)))#Bottom right corner of map red light
        addSprite(AnimatedSprite(game, self.animSpritePath+'redlight/0.png', (11.1, 1.1)))#Boss light 1
        addSprite(AnimatedSprite(game, self.animSpritePath+'redlight/0.png', (11.1, 2.9)))#Boss light 2

        #NPC map
        addNpc(Soldier(game))
        addNpc(Soldier(game, pos=(5.1, 7.5)))
        addNpc(Soldier(game, pos=(6.1, 6.5)))
        addNpc(Soldier(game, pos=(8.5, 5.5)))
        addNpc(Soldier(game, pos=(9.8, 2.1)))
        addNpc(Soldier(game, pos=(9.2, 7.2)))
        addNpc(Soldier(game, pos=(14.1, 1.1)))
        addNpc(Soldier(game, pos=(14.5,3.5)))
        addNpc(Cacodemon(game, pos=(7.1, 5)))
        addNpc(Cacodemon(game, pos=(9.5, 1.5)))
        addNpc(Cacodemon(game, pos=(14.8, 7.8)))
        addNpc(Cacodemon(game, pos=(13.1, 4.4)))

    def update(self):
        self.npcPositions = {npc.mapPos for npc in self.npcList if npc.alive}
        [sprite.update() for sprite in self.spriteList]
        [npc.update() for npc in self.npcList]

    def addNpc(self, npc):
        self.npcList.append(npc)

    def addSprite(self, sprite):
        self.spriteList.append(sprite)