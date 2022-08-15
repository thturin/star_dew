import pygame
from settings import *
from player import Player

class Level:
    def __init__(self):

        #get the display surface
        self.display_surface = pygame.display.get_surface()

        #sprite groups
        self.all_sprites = pygame.sprite.Group()

        self.setup()

    def setup(self):
        self.player = Player((640,360),self.all_sprites)

    def run(self,dt):
        #print('run game')
        self.display_surface.fill('pink')
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)
