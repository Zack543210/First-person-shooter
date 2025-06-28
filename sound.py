import pygame as pg

class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'music/'
        self.shotgun = pg.mixer.Sound(self.path + 'shotgun.wav')
        self.npcPain = pg.mixer.Sound(self.path + 'npcPain.wav')
        self.npcDeath = pg.mixer.Sound(self.path + 'npcDeath.wav')
        self.npcShot = pg.mixer.Sound(self.path + 'npcAttack.wav')
        self.playerPain = pg.mixer.Sound(self.path + 'playerPain.wav')
        self.theme = pg.mixer.music.load(self.path + 'theme.mp3')
        pg.mixer.music.play()