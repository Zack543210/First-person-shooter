from settings import *


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.shot = False
        self.health = PLAYER_MAX_HEALTH
        self.rel = 0
        self.healthRecoveryDelay = GAME_LEVEL
        self.timePrev = pg.time.get_ticks()

    def recoverHealth(self):
        if self.checkHealthRecoveryDelay() and self.health < PLAYER_MAX_HEALTH:
            self.health += 1

    def checkHealthRecoveryDelay(self):
        timeNow = pg.time.get_ticks()
        if timeNow - self.timePrev > self.healthRecoveryDelay*100:
            self.timePrev = timeNow
            return True

    def checkGameOver(self):
        if self.health < 1:
            self.game.objectRenderer.gameOver()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.newGame()

    def getDamage(self, damage):
        self.health -= damage
        self.game.objectRenderer.playerDamage()
        self.game.sound.playerPain.play()
        self.checkGameOver()
    
    def fire(self):
        self.game.sound.shotgun.play()
        self.shot = True
        self.game.weapon.reloading = True

    def singleFireEvent(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                self.fire()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE and not self.shot and not self.game.weapon.reloading:
                self.fire()

    def movement(self):
        sinA = math.sin(self.angle)
        cosA = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.deltaTime
        speedSin = speed * sinA
        speedCos = speed * cosA

        keys = pg.key.get_pressed()
        if keys[pg.K_w] or keys[pg.K_UP]:
            dx += speedCos
            dy += speedSin
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            dx += -speedCos
            dy += -speedSin
        if keys[pg.K_a]:
            dx += speedSin
            dy += -speedCos
        if keys[pg.K_d]:
            dx += -speedSin
            dy += speedCos

        self.checkWallCollision(dx, dy)
        
        if keys[pg.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED * self.game.deltaTime
        if keys[pg.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED * self.game.deltaTime
        self.angle %= math.tau

    def checkWall(self, x, y):
        return (x, y) not in self.game.map.worldMap
    
    def checkWallCollision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.deltaTime
        if self.checkWall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.checkWall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def draw(self):
        pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100), (self.x * 100 + WIDTH * math.cos(self.angle),
                      self.y * 100 + WIDTH * math.sin(self.angle)), 2)
        
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def mouseControl(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx < MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.deltaTime

    def update(self):
        self.movement()
        self.mouseControl()
        self.recoverHealth()

    @property
    def pos(self):
        return self.x, self.y
    
    @property
    def mapPos(self):
        return int(self.x), int(self.y)