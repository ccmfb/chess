import pygame
import settings
import event_handler
import pieces as pi

BOARD_DARK = (127, 85, 57)
BOARD_LIGHT = (221, 184, 146)

class Game:
	def __init__(self):
		pygame.init()
		pygame.font.init()
		pygame.display.set_caption('Chess')
		settings.init()

		self.screen = pygame.display.set_mode((800, 600))
		self.surface_moves = pygame.Surface((800,600), pygame.SRCALPHA)
		self.clock = pygame.time.Clock()

		self.board_pos = [[(30 + (x * 60), 30 + (y * 60)) for x in range(8)] for y in range(8)]

		self.create_pieces()
		self.event_handler = event_handler.Event_Handler()

	# Could go into settings
	def create_pieces(self):
		
		# General List     W   B
		self.all_pieces = [[],[]]

		# ------ White Pieces ------
		self.all_pieces[0].append([pi.Pawn(self.set_pos(x, 1), 'w') for x in range(8)])
		self.all_pieces[0].append([pi.Rock(self.set_pos(0, 0), 'w'), pi.Rock(self.set_pos(7,0), 'w')])
		self.all_pieces[0].append([pi.Knight(self.set_pos(1,0), 'w'), pi.Knight(self.set_pos(6,0), 'w')])
		self.all_pieces[0].append([pi.Bishop(self.set_pos(2,0), 'w'), pi.Bishop(self.set_pos(5,0), 'w')])
		self.all_pieces[0].append([pi.Queen(self.set_pos(3,0), 'w')])
		self.all_pieces[0].append([pi.King(self.set_pos(4,0), 'w')])

		# ------ Black Pieces ------
		self.all_pieces[1].append([pi.Pawn(self.set_pos(x, 6), 'b') for x in range(8)])
		self.all_pieces[1].append([pi.Rock(self.set_pos(0,7), 'b'), pi.Rock(self.set_pos(7,7), 'b')])
		self.all_pieces[1].append([pi.Knight(self.set_pos(1,7), 'b'), pi.Knight(self.set_pos(6,7), 'b')])
		self.all_pieces[1].append([pi.Bishop(self.set_pos(2,7), 'b'), pi.Bishop(self.set_pos(5,7), 'b')])
		self.all_pieces[1].append([pi.Queen(self.set_pos(3,7), 'b')])
		self.all_pieces[1].append([pi.King(self.set_pos(4,7), 'b')])

	def run(self):

		# Game loop
		while settings.running:
			
			# Check for events
			self.event_handler.check_events(self.all_pieces)

			# Draw
			self.surface_moves.fill((255,255,255,0))
			self.draw_board()

			for colou in self.all_pieces:
				for typ in colou:
					for piece in typ:
						piece.draw(self.screen, self.surface_moves)

			pygame.display.flip()
			self.clock.tick(60)

		# When loop is ended quit pygame
		pygame.quit()

	def draw_board(self):
		self.screen.fill((230, 230, 230))

		colour_dict = {True: BOARD_LIGHT, False: BOARD_DARK}
		current_colour = True
		for row in range(8):
			for square in range(8):
				pygame.draw.rect(self.screen, colour_dict[current_colour], (square * 60, row * 60, 60, 60))
				current_colour = not current_colour
			current_colour = not current_colour

	def set_pos(self, x, y):
		return self.board_pos[y][x]
			

if __name__ == '__main__':
	game = Game()
	game.run()
