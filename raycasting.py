from settings import *


class Raycasting:
    def __init__(self, game):
        self.game = game
        self.raycastingResult = []
        self.objectsToRender = []
        self.textures = self.game.objectRenderer.wallTextures

    def getobjectsToRender(self):
        self.objectsToRender = []
        for ray, values in enumerate(self.raycastingResult):
            depth, projHeight, texture, offset = values

            offset = offset % 1.0 #if error put this line in the if statement
            if projHeight < HEIGHT:

                wallColumn = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wallColumn = pg.transform.scale(wallColumn, (SCALE, projHeight))
                wallPos = (ray * SCALE, HALF_HEIGHT - projHeight // 2)
            else:
                textureHeight = TEXTURE_SIZE * HEIGHT / projHeight
                wallColumn = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - textureHeight // 2,
                    SCALE, textureHeight
                )
                wallColumn = pg.transform.scale(wallColumn, (SCALE, HEIGHT))
                wallPos = (ray * SCALE, 0)

            self.objectsToRender.append((depth, wallColumn, wallPos))

    def raycast(self):
        self.raycastingResult = []
        textureHor, textureVert = 1, 1
        ox, oy = self.game.player.pos
        xMap, yMap = self.game.player.mapPos

        rayAngle = self.game.player.angle - HALF_FOV + 0.0001
        for _ in range(NUM_RAYS):
            sinA = math.sin(rayAngle)
            cosA = math.cos(rayAngle)

            #horizontals
            yHor, dy = (yMap + 1, 1) if sinA > 0 else (yMap - 1e-6, -1)
            depthHor = (yHor - oy) / sinA
            xHor = ox + depthHor * cosA

            deltaDepth = dy / sinA
            dx = deltaDepth * cosA

            for _ in range(MAX_DEPTH):
                tileHor = int(xHor), int(yHor)
                if tileHor in self.game.map.worldMap:
                    textureHor = self.game.map.worldMap[tileHor]
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

            for _ in range(MAX_DEPTH):
                tileVert = int(xVert), int(yVert)
                if tileVert in self.game.map.worldMap:
                    textureVert = self.game.map.worldMap[tileVert]
                    break
                xVert += dx
                yVert += dy
                depthVert += deltaDepth

            #depth, textureOffset
            if depthVert < depthHor:
                depth, texture = depthVert, textureVert
                yVert %= 1
                offset = yVert if cosA > 0 else (1 - yVert)
            else:
                depth, texture = depthHor, textureHor
                xVert %= 1
                offset = (1 - xHor) if sinA < 0 else xHor

            depth *= math.cos(self.game.player.angle - rayAngle) # remove fisheye effect

            #projection
            projHeight = SCREEN_DIST / (depth + 0.0001)

            #raycasting result
            self.raycastingResult.append((depth, projHeight, texture, offset))

            rayAngle += DELTA_ANGLE

    def update(self):
        self.raycast()
        self.getobjectsToRender()