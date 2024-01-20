import pygame
from support import importCsvLayout, import_cut_graphics
from settings import tile_size, screen_height, screen_width, dogCount
from tiles import Tile, StaticTile, Crate, Animal, Palm

from decoration import Sky, Water
from player import Player
from particles import ParticleEffect
from game_data import levels


class Level:
	def __init__(self, current_level, surface, makeMenu, changeAnimals):
		self.displaySurface = surface
		self.scrollSpeed = 0
		self.current_x = None
		self.maxSpriteCount = 6
		self.animalSpriteCount = 0
		self.dogSpriteCount = 0
		self.winScore = dogCount
		self.animalSpriteDict = {}
		self.score = 0

		self.animalCollectSound = pygame.mixer.Sound('../audio/effects/coin.wav')
		self.stomp_sound = pygame.mixer.Sound('../audio/effects/stomp.wav')

		self.makeMenu = makeMenu
		self.current_level = current_level
		levelData = levels[self.current_level]
		self.new_max_level = levelData['unlock']

		playerLayout = importCsvLayout(levelData['player'])
		self.player = pygame.sprite.GroupSingle()
		self.goal = pygame.sprite.GroupSingle()
		self.makePlayer(playerLayout)

		self.changeAnimals = changeAnimals

		self.dustFX = pygame.sprite.GroupSingle()
		self.isPlayerGrounded = False

		self.explosionFX = pygame.sprite.Group()

		terrainLayout = importCsvLayout(levelData['terrain'])
		self.terrain_sprites = self.create_tile_group(terrainLayout, 'terrain')

		grassLayout = importCsvLayout(levelData['grass'])
		self.grass_sprites = self.create_tile_group(grassLayout, 'grass')

		crateLayout = importCsvLayout(levelData['crates'])
		self.crate_sprites = self.create_tile_group(crateLayout, 'crates')

		animal_layout = importCsvLayout(levelData['animal'])
		self.animal_sprites = self.create_tile_group(animal_layout, 'animal')
		self.all_animal_sprites = self.animal_sprites
		print(self.animal_sprites)

		fg_palm_layout = importCsvLayout(levelData['fg palms'])
		self.fg_palm_sprites = self.create_tile_group(fg_palm_layout, 'fg palms')

		bg_palm_layout = importCsvLayout(levelData['bg palms'])
		self.bg_palm_sprites = self.create_tile_group(bg_palm_layout, 'bg palms')

		constraint_layout = importCsvLayout(levelData['constraints'])
		self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraint')

		self.sky = Sky(8)
		level_width = len(terrainLayout[0]) * tile_size
		self.water = Water(screen_height - 20, level_width)

	def create_tile_group(self, layout, type):
		sprite_group = pygame.sprite.Group()

		for row_index, row in enumerate(layout):
			for col_index, val in enumerate(row):
				if val != '-1':
					x = col_index * tile_size
					y = row_index * tile_size

					if type == 'terrain':
						terrain_tile_list = import_cut_graphics('../graphics/terrain/terrain_tiles.png')
						tile_surface = terrain_tile_list[int(val)]
						sprite = StaticTile(tile_size, x, y, tile_surface)

					if type == 'grass':
						grass_tile_list = import_cut_graphics('../graphics/decoration/grass/grass.png')
						tile_surface = grass_tile_list[int(val)]
						sprite = StaticTile(tile_size, x, y, tile_surface)

					if type == 'crates':
						sprite = Crate(tile_size, x, y)

					if type == 'animal':
						if self.animalSpriteCount <= self.maxSpriteCount:

							if self.dogSpriteCount < self.winScore:
								sprite = Animal(tile_size, x, y, 'dog')
								self.dogSpriteCount +=1
							else: sprite = Animal(tile_size, x, y, 'cat')
							self.animalSpriteCount += 1
				


					if type == 'fg palms':
						if val == '0': sprite = Palm(tile_size, x, y, '../graphics/terrain/palm_small', 38)
						if val == '1': sprite = Palm(tile_size, x, y, '../graphics/terrain/palm_large', 64)

					if type == 'bg palms':
						sprite = Palm(tile_size, x, y, '../graphics/terrain/palm_bg', 64)

					if type == 'constraint':
						sprite = Tile(tile_size, x, y)
					if (sprite != None):
						sprite_group.add(sprite)

		return sprite_group

	def makePlayer(self, layout):
		for row_index, row in enumerate(layout):
			for col_index, val in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size
				if val == '0':
					sprite = Player((x, y), self.displaySurface, self.makeJumpFX)
					self.player.add(sprite)
				if val == '1':
					hat_surface = pygame.image.load('../graphics/character/hat.png').convert_alpha()
					sprite = StaticTile(tile_size, x, y, hat_surface)
					self.goal.add(sprite)

	def makeJumpFX(self, pos):
		if self.player.sprite.facing_right:
			pos -= pygame.math.Vector2(10, 5)
		else:
			pos += pygame.math.Vector2(10, -5)
		jump_particle_sprite = ParticleEffect(pos, 'jump')
		self.dustFX.add(jump_particle_sprite)

	def horizontal_movement_collision(self):
		player = self.player.sprite
		player.collision_rect.x += player.direction.x * player.speed
		collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()
		for sprite in collidable_sprites:
			if sprite.rect.colliderect(player.collision_rect):
				if player.direction.x < 0:
					player.collision_rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				elif player.direction.x > 0:
					player.collision_rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right

	def vertical_movement_collision(self):
		player = self.player.sprite
		player.simulateGravity()
		collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()

		for sprite in collidable_sprites:
			if sprite.rect.colliderect(player.collision_rect):
				if player.direction.y > 0:
					player.collision_rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.collision_rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True

		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False

	def scroll_x(self):
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < screen_width / 4 and direction_x < 0:
			self.scrollSpeed = 8
			player.speed = 0
		elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
			self.scrollSpeed = -8
			player.speed = 0
		else:
			self.scrollSpeed = 0
			player.speed = 8

	def get_isPlayerGrounded(self):
		if self.player.sprite.on_ground:
			self.isPlayerGrounded = True
		else:
			self.isPlayerGrounded = False

	def create_landing_dust(self):
		if not self.isPlayerGrounded and self.player.sprite.on_ground and not self.dustFX.sprites():
			if self.player.sprite.facing_right:
				offset = pygame.math.Vector2(10, 15)
			else:
				offset = pygame.math.Vector2(-10, 15)
			fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
			self.dustFX.add(fall_dust_particle)

	def check_death(self):
		if self.player.sprite.rect.top > screen_height:
			self.makeMenu(self.current_level, 0)

	def check_win(self):
		if pygame.sprite.spritecollide(self.player.sprite, self.goal,False) and self.score >= self.winScore:
			self.makeMenu(self.current_level, self.new_max_level)

	def check_animal_collisions(self):
		collided_animals = pygame.sprite.spritecollide(self.player.sprite, self.animal_sprites, False)
		if collided_animals:
			self.animalCollectSound.play()
			for animal in collided_animals:
				if animal.type == 'dog':
					self.score+=1
					self.changeAnimals(1)
					self.animalSpriteCount -= 1
					animal.kill()
					# if animal in self.animal_sprites:
					# 	# self.animal_sprites.remove(animal)
					# 	self.animalSpriteCount -= 1
					# 	# spriteList = list(self.animal_sprites)
					# 	# randIdx = random.randint(0, len(self.all_animal_sprites)-1)
					# 	# newSprite = spriteList[randIdx]
					# 	# self.animal_sprites.add(newSprite)
					# 	animal.kill()
				elif animal.type == 'cat':
					self.animalSpriteCount -= 1
					animal.kill()




				# print(animal.type)
				# if self.animalSpriteClassifier(animal):
				# 	animal.kill()
				# self.changeAnimals(1)
				# self.animalSpriteCount -= 1

	# def animalSpriteClassifier(self, animal):
	# 	print("classifier called")
	#
	# 	print(self.animalSpriteDict)
	# 	if animal.type == 'Dog':
	# 		for animalInLevel in self.animal_sprites:
	#
	# 			if animal == animalInLevel:
	# 				if animal.image in self.animalSpriteDict['dog']:
	# 					return True
	# 					print("Dog")
	# 				elif animal.image in self.animalSpriteDict['cat']:
	# 					return True
	# 					print("Cat")
	# 				else:
	# 					print("Invalid img")
	# 					return False
	#
	# 	return False

	# if animal.image in self.animal_sprites:
	# 	print("Cat")
	# if animal.image in self.animalSpriteDict['dog']:
	# 	print("Dog")
	# else: print("invalid img")

	def run(self):

		# sky
		self.sky.draw(self.displaySurface)

		
		self.bg_palm_sprites.update(self.scrollSpeed)
		self.bg_palm_sprites.draw(self.displaySurface)

		self.dustFX.update(self.scrollSpeed)
		self.dustFX.draw(self.displaySurface)

		self.terrain_sprites.update(self.scrollSpeed)
		self.terrain_sprites.draw(self.displaySurface)

		self.constraint_sprites.update(self.scrollSpeed)
	
		self.explosionFX.update(self.scrollSpeed)
		self.explosionFX.draw(self.displaySurface)

		self.crate_sprites.update(self.scrollSpeed)
		self.crate_sprites.draw(self.displaySurface)

		self.grass_sprites.update(self.scrollSpeed)
		self.grass_sprites.draw(self.displaySurface)

		self.animal_sprites.update(self.scrollSpeed)
		self.animal_sprites.draw(self.displaySurface)

		self.fg_palm_sprites.update(self.scrollSpeed)
		self.fg_palm_sprites.draw(self.displaySurface)

		self.check_animal_collisions()
		self.player.update()
		self.horizontal_movement_collision()

		self.get_isPlayerGrounded()
		self.vertical_movement_collision()
		self.create_landing_dust()

		self.scroll_x()
		self.player.draw(self.displaySurface)
		self.goal.update(self.scrollSpeed)
		self.goal.draw(self.displaySurface)

		self.check_death()

		self.water.draw(self.displaySurface, self.scrollSpeed)
