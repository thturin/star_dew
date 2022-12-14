import pygame
from settings import *
from support import *
from timer import *

class Player(pygame.sprite.Sprite): #must inherit sprite class from pygame

    def __init__(self,pos,group):
        super().__init__(group)

        self.import_assets() #has to be at the top
        self.status = 'down_idle'
        self.frame_index = 0

        #general setup attributes
        self.image = self.animations[self.status][self.frame_index]

        self.rect = self.image.get_rect(center = pos)
        self.z = LAYERS['main'] #[x,y,z] position where z is depth for 3 dimension

        #movement attributes
        self.direction = pygame.math.Vector2() #[x,y]
        self.pos = pygame.math.Vector2(self.rect.center) #position is not scored in the rectangle, instead in a vector
        self.speed = 200

        #tools
        self.tools = ['hoe','axe','water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        #seed
        self.seeds = ['corn','tomato']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]

        # timers
        self.timers = {
            'tool use': Timer(350, self.use_tool()),
            'tool switch': Timer(200), #we dont want to call another function after
            'seed use': Timer(350,self.use_seed()),
            'seed switch': Timer(200)
        }

    def use_tool(self):
        print(self.selected_tool)

    def use_seed(self):
        print(self.selected_seed)

    def import_assets(self):
        self.animations = { 'up':[],'down':[],'left':[],'right':[],
                            'up_idle':[],'down_idle':[],'left_idle':[],'right_idle':[],
                            'up_hoe': [], 'down_hoe': [], 'left_hoe': [], 'right_hoe': [],
                            'up_axe': [], 'down_axe': [], 'left_axe': [], 'right_axe': [],
                            'up_water': [], 'down_water': [], 'left_water': [], 'right_water': []
        }

        for animation in self.animations.keys():
            full_path = 'graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)
        #print(self.animations) #'up': [<Surface(172x124x32 SW)>, <Surface(172x124x32 SW)>, <Surface(172x124x32 SW)>, <Surface(172x124x32 SW)>],

    def animate(self,dt):
        self.frame_index +=4 * dt
        #('this is frame_index = '+str(int(self.frame_index)))
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()
        #directions
        if not self.timers['tool use'].active: #if the tool use timer is not active, then a tool is not in use so you can MOVE. This prohibits player from moving when using tool
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y=1
                self.status = 'down'
            else: #If we are not pressing
                self.direction.y=0
            if keys[pygame.K_LEFT]:
                self.direction.x=-1
                self.status = 'left'
            elif keys[pygame.K_RIGHT]:
                self.direction.x=1
                self.status = 'right'
            else: #you need this else because if the left or right key is not being pressed, stop goin in that direction
                self.direction.x=0


            #tool use
            if keys[pygame.K_SPACE]:
                self.timers['tool use'].activate() #activate the tool use timer
                self.direction = pygame.math.Vector2() #stop player from moving
                self.frame_index=0 #reset

            #change tool
            if keys[pygame.K_q] and not self.timers['tool switch'].active: #tool switch timer can't be active
                self.timers['tool switch'].activate()
                self.tool_index+=1
                # if self.tool_index >= len(self.selected_tool):
                #     self.tool_index=0 #same thing as below
                self.tool_index = self.tool_index if self.tool_index < len(self.tools) else 0
                self.selected_tool = self.tools[self.tool_index]
                #print('The tool selected is {}'.format(self.selected_tool[self.tool_index]))
                print(self.selected_tool)

            #seed use
            if keys[pygame.K_LCTRL]:
                self.timers['seed use'].activate() #set time for see use
                self.direction = pygame.math.Vector2() #stop player from moving
                self.frame_index = 0 #reset the frame index to 0 for full animation
                print('use seed ') #no animation for seed yet so this print function will do for now

            #change seed
            if keys[pygame.K_e] and not self.timers['seed switch'].active:
                self.timers['seed switch'].activate()
                self.seed_index+=1
                self.seed_index = self.seed_index if self.seed_index < len(self.seeds) else 0
                #print('the index is {}'.format(self.seed_index))
                self.selected_seed = self.seeds[self.seed_index]
                print(self.selected_seed)



    def get_status(self):
        #idle use
        if self.direction.magnitude()==0: #if the player is not moving
            self.status = self.status.split('_')[0]+'_idle' #add idle to the status

        #tool use
        if self.timers['tool use'].active: #if the tool used timer is active
            self.status = self.status.split('_')[0]+'_' + self.selected_tool

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def move(self,dt):

        #you must normalize the vector to prevent diagonal travel from going too fast -> take hypotenuse length and turns it into unit hypotenuse
        if self.direction.magnitude()>0:#if vector is [0,0] than, you can't normalize
            self.direction = self.direction.normalize()
            #print(self.direction)

        #horizontal movement
        self.pos.x += self.direction.x *self.speed *dt
        self.rect.centerx = self.pos.x
        #vertical movement
        self.pos.y +=self.direction.y *self.speed *dt
        self.rect.centery = self.pos.y

    def update(self,dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.move(dt)
        self.animate(dt)