import pygame, sys
from settings import *
from level import Level


class Game:
    def __init__(self):
        pygame.init() #initiate pygame
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT)) #create a screen
        pygame.display.set_caption('Sprout Land')
        self.clock = pygame.time.Clock() #create a clock attribute
        self.level = Level() #the game has a level attribute

    def run(self): #where the game runs
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #if any event quits
                    pygame.quit()
                    sys.exit()#exit the game
            dt = self.clock.tick() / 1000 #delta time
            #self.clock.tick(20)/1000 check to see the different frame rates and how it affects the player movement
            """
            Delta Time is the time difference between the current and the previous frame 
            How long it takes for the computer to draw the current frame
            Multiplying this number with any movement in the game will make it run consistent
            """
            self.level.run(dt) #run the level (update it)
            pygame.display.update() #update display

if __name__ == '__main__':
    game = Game() #create an object game
    game.run()