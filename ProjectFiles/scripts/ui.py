import pygame

class UI:
	def __init__(self,surface):

		self.display_surface = surface 

		self.scoreIcon = pygame.image.load('../graphics/ui/score.png').convert_alpha()
		self.scoreIcon = pygame.transform.scale(self.scoreIcon, (64,64))
		self.scoreIconRect = self.scoreIcon.get_rect(topleft = (50,61))
		self.font = pygame.font.Font('../graphics/ui/ARCADEPI.ttf',20)


	def displayAnimalCount(self,amount):
		self.display_surface.blit(self.scoreIcon,self.scoreIconRect)
		animal_count_surf = self.font.render(str(amount),False,'#000000')
		animal_count_rect = animal_count_surf.get_rect(midleft = (self.scoreIconRect.right + 4,self.scoreIconRect.centery))
		self.display_surface.blit(animal_count_surf,animal_count_rect)
		
	def show_objective_text1(self):
		text = 'Collect 4 dog sprites'
		text1Surf =  self.font.render(text,False,'#000000')
		text1Rect = text1Surf.get_rect(midleft = (480,self.scoreIconRect.centery))
		self.display_surface.blit(text1Surf, text1Rect)

	def show_objective_text2(self):
		text = 'Now reach the end of the level to finish'
		text2Surf =  self.font.render(text,False,'#000000')
		text2Rect = text2Surf.get_rect(midleft = (480,self.scoreIconRect.centery))
		self.display_surface.blit(text2Surf, text2Rect)



		
			