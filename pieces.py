import pygame
import operator

WHITE_PIECES = (220,220,220)
BLACK_PIECES = (192,192,192)

class Piece:
	def __init__(self, position, colour):
		self.showing_moves = False
		self.colour = colour
		self.colour_rgb = WHITE_PIECES if self.colour == 'w' else BLACK_PIECES

		self.piece_rect = pygame.Rect(position[0] - 15, position[1] - 15, 30, 30)
		self.moves = []
		self.move_rects = []
		self.beat_rects = []

		self.x_bound_left = 0
		self.x_bound_right = 480
		self.y_bound_top = 0
		self.y_bound_bottom = 480

		self.font = pygame.font.SysFont('Helvetica Neue', 15)

	def update_moves(self, all_pieces):
		self.move_rects = []
		self.beat_rects = []

		for mov_type in self.moves:						
			for mov in mov_type:

				# Check for board boundaries
				if self.x_bound_left < self.piece_rect.x + mov[0] < self.x_bound_right:
					if self.y_bound_top < self.piece_rect.y + mov[1] < self.y_bound_bottom:
						self.move_rects.append(pygame.Rect(self.piece_rect.x + mov[0], self.piece_rect.y + mov[1], 30, 30))

		for mov_type in self.moves:
			for mov in mov_type:
				for team in all_pieces:
					for type_of_piece in team:
						for piece in type_of_piece:
							
							# Check for other pieces
							if self.colour == 'w':
								if piece.colour == 'w':
									if self.piece_rect.x + mov[0] == piece.piece_rect.x and self.piece_rect.y + mov[1] == piece.piece_rect.y:
										if piece.piece_rect in self.move_rects:
											self.move_rects.remove(piece.piece_rect)
											self.remove_further_moves(mov)
								if piece.colour == 'b':
									if self.piece_rect.x + mov[0] == piece.piece_rect.x and self.piece_rect.y + mov[1] == piece.piece_rect.y:
										if piece.piece_rect in self.move_rects:
											self.move_rects.append(pygame.Rect(self.piece_rect.x + mov[0], self.piece_rect.y + mov[1], 30, 30))
											self.beat_rects.append(pygame.Rect(self.piece_rect.x + mov[0] - 10, self.piece_rect.y + mov[1] - 10, 50, 50))
											self.remove_further_moves(mov)

							if self.colour == 'b':
								if piece.colour == 'b':
									if self.piece_rect.x + mov[0] == piece.piece_rect.x and self.piece_rect.y + mov[1] == piece.piece_rect.y:
										if piece.piece_rect in self.move_rects:
											self.move_rects.remove(piece.piece_rect)
											self.remove_further_moves(mov)
								if piece.colour == 'w':
									if self.piece_rect.x + mov[0] == piece.piece_rect.x and self.piece_rect.y + mov[1] == piece.piece_rect.y:
										if piece.piece_rect in self.move_rects:
											self.move_rects.append(pygame.Rect(self.piece_rect.x + mov[0], self.piece_rect.y + mov[1], 30, 30))
											self.beat_rects.append(pygame.Rect(self.piece_rect.x + mov[0] - 10, self.piece_rect.y + mov[1] - 10, 50, 50))
											self.remove_further_moves(mov)

	def remove_further_moves(self, move):
		to_delete_moves = []
		for mov_type in self.moves:
			if move in mov_type:
				index = mov_type.index(move)
				to_delete_moves = mov_type[index:]

		for mov in to_delete_moves:
			if pygame.Rect(self.piece_rect.x + mov[0], self.piece_rect.y + mov[1], 30, 30) in self.move_rects:
				self.move_rects.remove(pygame.Rect(self.piece_rect.x + mov[0], self.piece_rect.y + mov[1], 30, 30))

	def move(self, all_white, all_black, to_x, to_y):	
		self.piece_rect.x = to_x
		self.piece_rect.y = to_y
		
	def draw(self, screen, surface_moves):
		pygame.draw.rect(screen, self.colour_rgb, self.piece_rect)
		screen.blit(self.textsurf,(self.piece_rect.x + 7, self.piece_rect.y + 7))

		if self.showing_moves:
			for rect in self.move_rects:
				pygame.draw.rect(surface_moves, (170, 0, 0, 80), rect)
			for rect in self.beat_rects:
				pygame.draw.rect(surface_moves, (170, 0, 0, 80), rect)

			screen.blit(surface_moves, (0,0))

class Pawn(Piece):
	def __init__(self, position, colour):
		super().__init__(position, colour)
		
		# 3 Possible ways of movement (normal, start pos, beating enemy)
		self.moves = [[],[]]

		if colour == 'w':
			self.moves[0].append((0,60))
			self.moves[1].append((0,120))
		elif colour == 'b':
			self.moves[0].append((0,-60))
			self.moves[1].append((0,-120))

		self.textsurf = self.font.render('P', False, (0,179,255))

	def update_moves(self, all_pieces):
		super().update_moves(all_pieces)

		if self.piece_rect.y != 75 and self.piece_rect.y != 375:
			if pygame.Rect(self.piece_rect.x + self.moves[1][0][0], self.piece_rect.y + self.moves[1][0][1], 30, 30) in self.move_rects:
				self.move_rects.remove(pygame.Rect(self.piece_rect.x + self.moves[1][0][0], self.piece_rect.y + self.moves[1][0][1], 30, 30))

class Rock(Piece):
	def __init__(self, position, colour):
		super().__init__(position, colour)

		# 4 Possible ways of movement
		self.moves = [
				[],[],[],[]
			]

		for i in range(7):
			self.moves[0].append((60 * (i+1), 0))
			self.moves[1].append((-60 * (i+1), 0))
			self.moves[2].append((0, 60 * (i+1)))
			self.moves[3].append((0, -60 * (i+1)))

		self.textsurf = self.font.render('R', False, (0,179,255))

class Knight(Piece):
	def __init__(self, position, colour):
		super().__init__(position, colour)

		# 8 Possible ways of movement
		self.moves = [
				[],[],[],[],[],[],[],[]
			]

		self.moves[0].append((60, -120))
		self.moves[1].append((120, -60))
		self.moves[2].append((120, 60))
		self.moves[3].append((60, 120))
		self.moves[4].append((-60, 120))
		self.moves[5].append((-120, 60))
		self.moves[6].append((-120, -60))
		self.moves[7].append((-60, -120))


		self.textsurf = self.font.render('Kn', False, (0,179,255))

class Bishop(Piece):
	def __init__(self, position, colour):
		super().__init__(position, colour)

		# 4 Possible movements
		self.moves = [
				[],[],[],[]
			]

		for i in range(7):
			self.moves[0].append((60*(i+1),60*(i+1)))
			self.moves[1].append((-60*(i+1),60*(i+1)))
			self.moves[2].append((60*(i+1),-60*(i+1)))
			self.moves[3].append((-60*(i+1),-60*(i+1)))

		self.textsurf = self.font.render('B', False, (0,179,255))

class Queen(Piece):
	def __init__(self, position, colour):
		super().__init__(position, colour)
		self.textsurf = self.font.render('Q', False, (0,179,255))

		# 8 Possible types of movement
		self.moves = [
				[],[],[],[],[],[],[],[]
			]

		for i in range(7):
			self.moves[0].append((60*(i+1),-60*(i+1)))
			self.moves[1].append((60*(i+1),60*(i+1)))
			self.moves[2].append((-60*(i+1),60*(i+1)))
			self.moves[3].append((-60*(i+1),-60*(i+1)))

		for i in range(7):
			self.moves[4].append((60 * (i+1), 0))
			self.moves[5].append((-60 * (i+1), 0))
			self.moves[6].append((0, 60 * (i+1)))
			self.moves[7].append((0, -60 * (i+1)))

class King(Piece):
	def __init__(self, position, colour):
		super().__init__(position, colour)

		# 8 Possible types of movement
		self.moves = [
				[],[],[],[],[],[],[],[]
			]

		self.moves[0].append((60,0))
		self.moves[1].append((-60,0))
		self.moves[2].append((0,60))
		self.moves[3].append((0,-60))

		self.moves[4].append((60,60))
		self.moves[5].append((-60,60))
		self.moves[6].append((60,-60))
		self.moves[7].append((-60,-60))

		self.textsurf = self.font.render('Ki', False, (0,179,255))

