from csv import reader
from settings import tile_size, player_sprite_size
import pygame
import os
from LR_Classifier import classifier
def import_folder(path, type):
    surface_list = []

    for _,__,image_files in os.walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            if(type=='player'):
                image_surf = pygame.transform.scale(image_surf, player_sprite_size)
            surface_list.append(image_surf)
            if(type=='animal'):
                print("Got animal")

    return surface_list

def importCsvLayout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map,delimiter = ',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map

def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surf = pygame.Surface((tile_size,tile_size),flags = pygame.SRCALPHA)
            new_surf.blit(surface,(0,0),pygame.Rect(x,y,tile_size,tile_size))
            cut_tiles.append(new_surf)

    return cut_tiles

def import_animal_sprites():
    images = {'cat': [], 'dog': []}  # Initialize 'cat' and 'dog' keys with empty lists
    path = '../graphics/animal'

    for img in os.listdir(path):
        if img.endswith(('.png', '.jpg', '.jpeg')):
            # key = random.choice(['cat', 'dog'])
            imgPath = os.path.join(path, img)
            image = pygame.image.load(imgPath).convert_alpha()

            clfr = classifier(imgPath)
            key = clfr.predict()
            print(key)

            images[key].append(image)  # Append the image to the list under the chosen key
            print("Adding image: ", images[key])

    return images





