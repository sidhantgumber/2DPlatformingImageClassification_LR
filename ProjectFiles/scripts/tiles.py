import pygame 
from support import import_folder, import_animal_sprites
import os
import random

class Tile(pygame.sprite.Sprite):
	def __init__(self,size,x,y):
		super().__init__()
		self.image = pygame.Surface((size,size))
		self.rect = self.image.get_rect(topleft = (x,y))

	def update(self,shift):
		self.rect.x += shift

class StaticTile(Tile):
	def __init__(self,size,x,y,surface):
		super().__init__(size,x,y)
		self.image = surface 

class Crate(StaticTile):
	def __init__(self,size,x,y):
		super().__init__(size,x,y,pygame.image.load('../graphics/terrain/crate.png').convert_alpha())
		offset_y = y + size
		self.rect = self.image.get_rect(bottomleft = (x,offset_y))

class AnimatedTile(Tile):
	def __init__(self,size,x,y,path):
		super().__init__(size,x,y)
		self.frames = import_folder(path,'generic')
		self.frame_index = 0
		self.image = self.frames[self.frame_index]

	def animate(self):
		self.frame_index += 0.15
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]

	def update(self,shift):
		self.animate()
		self.rect.x += shift

class Animal(Tile):
	def __init__(self, size, x, y, type):
		super().__init__(size, x, y)
		# self.spriteSurfaces = import_folder(path, 'animal')
		# self.image = random.choice(self.spriteSurfaces)
		# self.image = pygame.transform.scale(self.image, (128,128))
		self.animalDictionary = import_animal_sprites()
		self.dogImgList = self.animalDictionary['dog']
		self.catImgList = self.animalDictionary['cat']
		if type == 'dog':
			self.image = random.choice(self.dogImgList)
		else: self.image = random.choice(self.dogImgList)
		# self.dogImgList = self.animalDictionary['dog']
		# self.catImgList = self.animalDictionary['cat']
		# self.images = self.dogImgList + self.catImgList
		# self.image = random.choice(self.images)
		if self.image in self.dogImgList:
			self.type = 'dog'
		elif self.image in self.catImgList:
			self.type = 'cat'
		else: self.type = 'invalid'
		self.image = pygame.transform.scale(self.image, (128,128))


class Palm(AnimatedTile):
	def __init__(self,size,x,y,path,offset):
		super().__init__(size,x,y,path)
		offset_y = y - offset
		self.rect.topleft = (x,offset_y)