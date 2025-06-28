from spriteObject import *
from random import randint, random

class NPC(AnimatedSprite):
    def __init__(self, game, path='images/resources/sprites/npc/soldier/0.png',
                 pos=(5.1, 1.5), scale=0.6, shift=0.38, animationTime=180):
        super().__init__(game, path, pos, scale, shift, animationTime)
        self.attackImages = self.getImages(self.path + '/attack')
        self.deathImages = self.getImages(self.path + '/death')
        self.idleImages = self.getImages(self.path + '/idle')
        self.painImages = self.getImages(self.path + '/pain')
        self.walkImages = self.getImages(self.path + '/walk')

        self.attackDist = randint(3, SOLDIER_ATTACK_DIST)
        self.speed = 0.03
        self.size = 10
        self.health = SOLDIER_LIFE * 50
        self.attackDamage = 10
        self.accuracy = 0.2
        self.alive = True
        self.pain = False
        self.raycastValue = False
        self.frameCounter = 0
        self.playerSearchTrigger = False

    def update(self):
        self.checkAnimationTime()
        self.getSprite()
        self.runLogic()
        # self.drawRaycast()

    def checkWall(self, x, y):
        return (x, y) not in self.game.map.worldMap
    
    def checkWallCollision(self, dx, dy):
        if self.checkWall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.checkWall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def movement(self):
        # nextPos = self.game.player.mapPos #without pathfinding
        nextPos = self.game.pathfinding.getPath(self.mapPos, self.game.player.mapPos) #with pathfinding
        nextX, nextY = nextPos

        # pg.draw.rect(self.game.screen, 'gray', (100 * nextX, 100 * nextY, 100, 100))
        if nextPos not in self.game.objectHandler.npcPositions:
            angle = math.atan2(nextY + 0.5 - self.y, nextX + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.checkWallCollision(dx, dy)

    def attack(self):
        if self.animationTrigger:
            self.game.sound.npcShot.play()
            if random() < self.accuracy:
                self.game.player.getDamage(self.attackDamage)

    def animateDeath(self):
        if not self.alive:
            if self.game.globalTrigger and self.frameCounter < len(self.deathImages) - 1:
                self.deathImages.rotate(-1)
                self.image = self.deathImages[0]
                self.frameCounter += 1

    def animatePain(self):
        self.animate(self.painImages)
        if self.animationTrigger:
            self.pain = False
            self.health -= self.game.weapon.damage
            self.checkHealth()

    def checkHealth(self):
        if self.health < 1:
            self.alive = False
            self.game.sound.npcDeath.play()

    def checkHitInNpc(self):
        if self.raycastValue and self.game.player.shot:
            if HALF_WIDTH - self.spriteHalfWidth < self.screenX < HALF_WIDTH + self.spriteHalfWidth:
                self.game.sound.npcPain.play()
                self.game.player.shot = False
                self.pain = True

    def runLogic(self):
        if self.alive:
            self.raycastValue = self.raycastPlayerNpc()
            self.checkHitInNpc()
            if self.pain:
                self.animatePain()

            elif self.raycastValue:
                self.playerSearchTrigger = True

                if self.dist < self.attackDist:
                    self.animate(self.attackImages)
                    self.attack()
                else:
                    self.animate(self.walkImages)
                    self.movement()

            elif self.playerSearchTrigger:
                self.animate(self.walkImages)
                self.movement()

            else:
                self.animate(self.idleImages)
        else:
            self.animateDeath()

    @property
    def mapPos(self):
        return int(self.x), int(self.y)
    
    def raycastPlayerNpc(self):
        if self.game.player.mapPos == self.mapPos:
            return True
        
        wallDistV, wallDistH = 0, 0
        playerDistV, playerDistH = 0, 0

        ox, oy = self.game.player.pos
        xMap, yMap = self.game.player.mapPos

        rayAngle = self.theta

        sinA = math.sin(rayAngle)
        cosA = math.cos(rayAngle)

        #horizontals
        yHor, dy = (yMap + 1, 1) if sinA > 0 else (yMap - 1e-6, -1)
        depthHor = (yHor - oy) / sinA
        xHor = ox + depthHor * cosA

        deltaDepth = dy / sinA
        dx = deltaDepth * cosA

        for i in range(MAX_DEPTH):
            tileHor = int(xHor), int(yHor)
            if tileHor == self.mapPos:
                playerDistH = depthHor
                break
            if tileHor in self.game.map.worldMap:
                wallDistH = depthHor
                break
            xHor += dx
            yHor += dy
            depthHor += deltaDepth

        #verticles
        xVert, dx = (xMap + 1, 1) if cosA > 0 else (xMap - 1e-6, -1)

        depthVert = (xVert - ox) / cosA
        yVert = oy + depthVert * sinA

        deltaDepth = dx / cosA
        dy = deltaDepth * sinA

        for i in range(MAX_DEPTH):
            tileVert = int(xVert), int(yVert)
            if tileVert == self.mapPos:
                playerDistV = depthVert
                break
            if tileVert in self.game.map.worldMap:
                wallDistV = depthVert
                break
            xVert += dx
            yVert += dy
            depthVert += deltaDepth

        playerDist = max(playerDistV, playerDistH)
        wallDist = max(wallDistV, wallDistH)

        if 0 < playerDist < wallDist or not wallDist:
            return True
        return False
    
    def drawRaycast(self):
        pg.draw.circle(self.game.screen, 'red', (100 * self.x, 100 * self.y), 15)
        if self.raycastPlayerNpc():
            pg.draw.line(self.game.screen, 'orange', (100 * self.game.player.x, 100 * self.game.player.y),
                         (100 * self.x, 100 * self.y), 2)
            

class Soldier(NPC):
    def __init__(self, game, path='images/resources/sprites/npc/soldier/0.png',
                 pos=(5.1, 1.5), scale=0.6, shift=0.38, animationTime=180):
        super().__init__(game, path, pos, scale, shift, animationTime)

class Cacodemon(NPC):
    def __init__(self, game, path='images/resources/sprites/npc/cacodemon/0.png',
                 pos=(7.5, 4,2), scale=0.5, shift=0.9, animationTime=220): #Increase shift: Sprite Lower
        super().__init__(game, path, pos, scale, shift, animationTime)
        self.attackDist = 1
        self.health = 50 * CACAODEMON_LIFE
        self.attackDamage = 20
        self.speed = 0.05
        self.accuracy = 0.32