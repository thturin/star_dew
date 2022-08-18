import pygame
from settings import *

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS['main']):
        super().__init__(groups) #call the super class __init__  good for multiple inheritences as well
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z=z


class Water(Generic):
    def __init__(self, pos,frames,group):
        #animation setup
        self.frames = frames
        self.frame_index = 0

        #sprite setup
        super().__init__(pos=pos,surf=self.frames[self.frame_index],groups=group,z=LAYERS['water'])

    def animate(self,dt):
        self.frame_index += 5 * dt
        # ('this is frame_index = '+str(int(self.frame_index)))
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self,dt): #since you created an update class, this will be called in level.py when update is being called for sprite group
        self.animate(dt)


class WildFlower(Generic):
    def __init__(self, pos,surf,groups):
        super().__init__(pos,surf,groups)

class Tree(Generic):
    def __init__(self,pos,surf,groups, name):
        self.name=name
        super().__init__(pos,surf,groups)