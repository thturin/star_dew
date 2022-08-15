from os import walk
import pygame

def import_folder(path):
    surface_list = [] #store all of the surfaces

    for _,_,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image #graphics/character/right_water/1.png
            #print(full_path)
            image_surf = pygame.image.load(full_path).convert_alpha() #convert to alpha makes python run faster
            surface_list.append(image_surf)

    return surface_list