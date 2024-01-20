import pygame, sys
from settings import * 
from level import Level
from mainMenu import MainMenu
from ui import UI

class Game:
	def __init__(self):

		# game attributes
		self.maxLvl = 2
		self.animalsCollected = 0
		
		# audio 
		self.bgMusic = pygame.mixer.Sound('../audio/level_music.wav')
		self.mainMenuBgMusic = pygame.mixer.Sound('../audio/overworld_music.wav')

		# mainMenu creation
		self.mainMenu = MainMenu(0,self.maxLvl,screen,self.makeLevel)
		self.status = 'mainMenu'
		self.mainMenuBgMusic.play(loops = -1)

		# user interface 
		self.ui = UI(screen)


	def makeLevel(self,current_level):
		self.level = Level(current_level,screen,self.makeMenu,self.change_animalsCollected)
		self.status = 'level'
		self.mainMenuBgMusic.stop()
		self.bgMusic.play(loops = -1)

	def makeMenu(self,current_level,newMaxLvl):
		if newMaxLvl > self.maxLvl:
			self.maxLvl = newMaxLvl
		self.mainMenu = MainMenu(current_level,self.maxLvl,screen,self.makeLevel)
		self.status = 'mainMenu'
		self.mainMenuBgMusic.play(loops = -1)
		self.bgMusic.stop()

	def change_animalsCollected(self,amount):
		self.animalsCollected += amount


	def isGameOver(self):
		if self.level.check_win():
			self.animalsCollected = 0
			self.level.animalSpriteCount = 0
			self.maxLvl = 0
			self.level = None
			self.mainMenu = MainMenu(0,self.maxLvl,screen,self.makeLevel)
			self.status = 'mainMenu'
			self.bgMusic.stop()
			self.mainMenuBgMusic.play(loops = -1)

	def run(self):
		if self.status == 'mainMenu':
			self.mainMenu.run()
		else:
			self.level.run()
			self.ui.displayAnimalCount(self.animalsCollected)
			if self.animalsCollected >= dogCount:
				self.ui.show_objective_text2()
			else : self.ui.show_objective_text1()


			self.isGameOver()

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
game = Game()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	
	screen.fill('grey')
	game.run()

	pygame.display.update()
	clock.tick(60)