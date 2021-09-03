import pygame
import operator
import pieces as pi

BOARD_DARK = (127, 85, 57)
BOARD_LIGHT = (221, 184, 146)

class Game:
	def __init__(self):
		pygame.init()
		pygame.display.set_caption('Chess')
		self.screen = pygame.display.set_mode((800, 600))
		self.clock = pygame.time.Clock()

		self.board_pos = [[(80 + (x * 60), 90 + (y * 60)) for x in range(8)] for y in range(8)]

		self.create_pieces()

	def create_pieces(self):
		self.all_pieces = []
		self.all_white_pieces = []
		self.all_black_pieces = []

		# White
		self.white_pawns = [
			pi.Pawn(self.set_pos(x, 1), 'w') for x in range(8)
			]
		self.white_rocks = [pi.Rock(self.set_pos(0, 0), 'w'), pi.Rock(self.set_pos(7,0), 'w')]

		self.all_white_pieces.append(self.white_pawns)
		self.all_white_pieces.append(self.white_rocks)

		# Black
		self.black_pawns = [
			pi.Pawn(self.set_pos(x, 6), 'b') for x in range(8)
			]
		self.black_rocks = [pi.Rock(self.set_pos(0,7), 'b'), pi.Rock(self.set_pos(7,7), 'b')]

		self.all_black_pieces.append(self.black_pawns)
		self.all_black_pieces.append(self.black_rocks)

		# Complete list of every piece
		self.all_pieces.append(self.all_white_pieces)
		self.all_pieces.append(self.all_black_pieces)


	def run(self):
		running = True

		while running:
			for event in pygame.event.get():
				# QUIT
				if event.type == pygame.QUIT:
					running = False

				# Piece Interactions
				if event.type == pygame.MOUSEBUTTONDOWN:
					for colou in self.all_pieces:
						for typ in colou:	
							for piece in typ:
								if piece.showing_moves:
									for rect in piece.move_rects:
										if rect.collidepoint(event.pos):
											piece.move(self.all_white_pieces, self.all_black_pieces, rect.x, rect.y)

								piece.showing_moves = False

								# Showing possible moves
								if piece.piece_rect.collidepoint(event.pos):
									piece.update_moves(self.all_pieces)
									piece.showing_moves = True

			# Drawing
			self.draw_board()
			for colou in self.all_pieces:
				for typ in colou:
					for piece in typ:
						piece.draw(self.screen)

			pygame.display.flip()
			self.clock.tick(60)

		pygame.quit()

	def draw_board(self):
		self.screen.fill((230, 230, 230))

		colour_dict = {True: BOARD_LIGHT, False: BOARD_DARK}
		current_colour = True
		for row in range(8):
			for square in range(8):
				pygame.draw.rect(self.screen, colour_dict[current_colour], ((50 + (square * 60)), 60 + (row * 60), 60, 60))
				current_colour = not current_colour
			current_colour = not current_colour

	def set_pos(self, x, y):
		return self.board_pos[y][x]
			

if __name__ == '__main__':
	game = Game()
	game.run()