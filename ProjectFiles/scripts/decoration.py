from settings import vertical_tile_number, tile_size, screen_width, screen_height
import pygame
from tiles import AnimatedTile, StaticTile
from support import import_folder
from random import choice, randint

class Sky:
	def __init__(self,horizon,style = 'level'):
		self.top = pygame.image.load('../graphics/decoration/sky/sky.jpg').convert()
		self.top  = pygame.transform.scale(self.top, (screen_width, screen_height))
		self.horizon = horizon

		self.top = pygame.transform.scale(self.top,(screen_width,screen_height))

		self.style = style

	def draw(self,surface):
		surface.blit(self.top, (0,0))


class Water:
	def __init__(self,top,level_width):
		water_start = -screen_width
		water_tile_width = 192
		tile_x_amount = int((level_width + screen_width * 2) / water_tile_width)
		self.water_sprites = pygame.sprite.Group()

		for tile in range(tile_x_amount):
			x = tile * water_tile_width + water_start
			y = top
			sprite = AnimatedTile(192,x,y,'../graphics/decoration/water')
			self.water_sprites.add(sprite)

	def draw(self,surface,shift):
		self.water_sprites.update(shift)
		self.water_sprites.draw(surface)


