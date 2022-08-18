import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import *
from pytmx.util_pygame import load_pygame
from support import import_folder

class Level:
    def __init__(self):

        #get the display surface
        self.display_surface = pygame.display.get_surface()

        #sprite groups
        #pygame.sprite is a basic object class for sprites
        #self.all_sprites = pygame.sprite.Group()
        self.all_sprites = CameraGroup()

        self.setup()
        self.overlay = Overlay(self.player)

    def setup(self):
        tmx_data = load_pygame('data/map.tmx')

        #build the house
        for layer in ['HouseFloor','HouseFurnitureBottom']:
            for x,y, surf in tmx_data.get_layer_by_name(layer).tiles(): #getting all of the tiles inside of this layer
                Generic((x*TILE_SIZE,y*TILE_SIZE),surf,self.all_sprites,LAYERS['house bottom'])
        #
        for layer in ['HouseWalls','HouseFurnitureTop']:
            for x,y, surf in tmx_data.get_layer_by_name(layer).tiles(): #getting all of the tiles inside of this layer
                Generic((x*TILE_SIZE,y*TILE_SIZE),surf,self.all_sprites,LAYERS['main'])

        #fence
        for x,y, surf in tmx_data.get_layer_by_name('Fence').tiles():
            Generic((x*TILE_SIZE,y*TILE_SIZE),surf,self.all_sprites,LAYERS['main']) #its not necessary to write LAYERS['main'] because this is the z value by default

        #water
        water_frames = import_folder('graphics/water')
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
            Water((x*TILE_SIZE,y*TILE_SIZE), water_frames,self.all_sprites)

        #trees
        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree((obj.x,obj.y),obj.image,self.all_sprites, obj.name)
        #wildflowers
        for obj in tmx_data.get_layer_by_name('Decoration'):
            WildFlower((obj.x,obj.y),obj.image,self.all_sprites)

        self.player = Player((640, 360), self.all_sprites)
        Generic(pos=(0,0),surf=pygame.image.load('graphics/world/ground.png').convert_alpha(),groups=self.all_sprites,z=LAYERS['ground'])


    def run(self,dt):
        #print('run game')
        self.display_surface.fill('pink')
        #self.all_sprites.draw(self.display_surface)
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)

        self.overlay.display()

class CameraGroup(pygame.sprite.Group): #camera group class will inherit the pygame.sprite.group class properties and methods
    def __init__(self):
        super().__init__() #so the group works by itself
        self.display_surface = pygame.display.get_surface() #this camera group can draw on the display surface right away
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player): #this is the start for the camera logic
        self.offset.x =  player.rect.centerx - SCREEN_WIDTH /2
        self.offset.y =  player.rect.centery - SCREEN_HEIGHT /2
        for layer in LAYERS.values(): #this creates a 3 dimensional drawing of the canvas
            for sprite in sorted(self.sprites(),key= lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)


