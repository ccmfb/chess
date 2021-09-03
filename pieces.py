import pygame
import operator

WHITE_PIECES = (220,220,220)
BLACK_PIECES = (0,0,0)

class Piece:
	def __init__(self, position, colour):
		self.showing_moves = False
		self.colour = colour
		self.colour_rgb = WHITE_PIECES if self.colour == 'w' else BLACK_PIECES

		self.piece_rect = pygame.Rect(position[0] - 15, position[1] - 15, 30, 30)
		self.moves = []
		self.move_rects = []

	def update_moves(self, all_pieces):
		pass

	def move(self, all_white, all_black, to_x, to_y):	
		self.piece_rect.x = to_x
		self.piece_rect.y = to_y
		
	def draw(self, screen):
		pygame.draw.rect(screen, self.colour_rgb, self.piece_rect)

		if self.showing_moves:
			for rect in self.move_rects:
				pygame.draw.rect(screen, (170, 0, 0), rect)

class Pawn(Piece):
	def __init__(self, position, colour):
		super().__init__(position, colour)
		
		if colour == 'w':
			self.moves.append((0,60))
		elif colour == 'b':
			self.moves.append((0,-60))

	def update_moves(self, all_pieces):
		self.move_rects = []
		self.x_bound_left = 80
		self.x_bound_right = 500
		self.y_bound_top = 90
		self.y_bound_bottom = 510

		for mov in self.moves:
			if self.piece_rect.x + mov[0] + 15 >= 80 and self.piece_rect.x + mov[0] + 15 <= 500:
				if self.piece_rect.y + mov[1] + 15 >= 90 and self.piece_rect.y + mov[1] + 15 <= 510:
					for lis in all_pieces[0]:
						for piece in lis:
							if self.piece_rect.x + mov[0] != piece.piece_rect.x and self.piece_rect.y + mov[1] != piece.piece_rect.y:
								self.move_rects.append(pygame.Rect(self.piece_rect.x + mov[0], self.piece_rect.y + mov[1], 30, 30))



class Rock(Piece):
	def __init__(self, position, colour):
		super().__init__(position, colour)

		for i in range(7):
			self.moves.append((60 * (i+1), 0))
			self.moves.append((-60 * (i+1), 0))
			self.moves.append((0, 60 * (i+1)))
			self.moves.append((0, -60 * (i+1)))

	def update_moves(self, all_pieces):
		self.move_rects = []
		self.x_bound_left = 80
		self.x_bound_right = 500
		self.y_bound_top = 90
		self.y_bound_bottom = 510

		self.find_x_bound_left(all_pieces[0], all_pieces[1])
		self.find_x_bound_right(all_pieces[0], all_pieces[1])
		self.find_y_bound_top(all_pieces[0], all_pieces[1])
		self.find_y_bound_bottom(all_pieces[0], all_pieces[1])
		
		print('Bounds: ', self.x_bound_left, ', ', self.x_bound_right, ', ', self.y_bound_top, ', ', self.y_bound_bottom)
	
		for mov in self.moves:

			if self.piece_rect.x + mov[0] + 15 >= self.x_bound_left and self.piece_rect.x + mov[0] + 15 <= self.x_bound_right:
				if self.piece_rect.y + mov[1] + 15 < self.y_bound_bottom and self.piece_rect.y + mov[1] + 15 >= self.y_bound_top:

					# Append possible moves
					self.move_rects.append(pygame.Rect(self.piece_rect.x + mov[0], self.piece_rect.y + mov[1], 30, 30))

	def find_x_bound_left(self, all_white, all_black):
		if self.colour == 'w':
			team = all_white
		else:
			team = all_black

		for mov in self.moves:

			# Find x_bound_left
			for lis in team:
				for piece in lis:

					# Collision with other whites on x
					if self.piece_rect.x + mov[0] == piece.piece_rect.x:

						# left bound
						if self.piece_rect.x > piece.piece_rect.x:
							self.x_bound_left = piece.piece_rect.x + 30

	def find_x_bound_right(self, all_white, all_black):
		if self.colour == 'w':
			team = all_white
		else:
			team = all_black

		for mov in self.moves:

			# Find x_bound_right
			for lis in team:
				for piece in lis:

					# Collision with other whites on x
					if self.piece_rect.x + mov[0] == piece.piece_rect.x:
						# Right bound
						if self.piece_rect.x < piece.piece_rect.x:
							self.x_bound_right = piece.piece_rect.x + 15

	def find_y_bound_top(self, all_white, all_black):
		if self.colour == 'w':
			team = all_white
		else:
			team = all_black

		for mov in self.moves:

			# Find y_bound_top
			for lis in team:
				for piece in lis:

					# Collision with other whites on y
					if self.piece_rect.y + mov[1] == piece.piece_rect.y:

						# top bound
						if self.piece_rect.y > piece.piece_rect.y:
							self.y_bound_top = piece.piece_rect.y + 15
						

	def find_y_bound_bottom(self, all_white, all_black):
		if self.colour == 'w':
			team = all_white
		else:
			team = all_black

		for mov in self.moves:

			# Find y_bound_bottom
			for lis in team:
				for piece in lis:

					# Collision with other whites on y
					if self.piece_rect.y + mov[1] == piece.piece_rect.y:

						# bottom bound
						if self.piece_rect.y < piece.piece_rect.y:
							self.y_bound_bottom = piece.piece_rect.y + 15

class Knight(Piece):
	def __init__(self, position, colour):
		super().__init__(position, colour)

		self.moves.append((60, -120))
		self.moves.append((120, -60))
		self.moves.append((120, 60))
		self.moves.append((60, 120))
		self.moves.append((-60, 120))
		self.moves.append((-120, 60))
		self.moves.append((-120, -60))
		self.moves.append((-60, -120))

	def update_moves(self, all_pieces):
		self.move_rects = []
		for mov in self.moves:
			self.move_rects.append(pygame.Rect(self.piece_rect.x + mov[0], self.piece_rect.y + mov[1], 30, 30))

class Bishop(Piece):
	def __init__(self, position, colour):
		super().__init__(position, colour)

		for i in range(7):
			self.moves.append((60*(i+1),60*(i+1)))
			self.moves.append((-60*(i+1),60*(i+1)))
			self.moves.append((60*(i+1),-60*(i+1)))
			self.moves.append((-60*(i+1),-60*(i+1)))

	def update_moves(self, all_pieces):
		self.move_rects = []
		for mov in self.moves:
			self.move_rects.append(pygame.Rect(self.piece_rect.x + mov[0], self.piece_rect.y + mov[1], 30, 30))

class Queen(Piece):
	def __init__(self, position, colour):
		super().__init__(position, colour)

		for i in range(7):
			self.moves.append((60*(i+1),60*(i+1)))
			self.moves.append((-60*(i+1),60*(i+1)))
			self.moves.append((60*(i+1),-60*(i+1)))
			self.moves.append((-60*(i+1),-60*(i+1)))

		for i in range(7):
			self.moves.append((60 * (i+1), 0))
			self.moves.append((-60 * (i+1), 0))
			self.moves.append((0, 60 * (i+1)))
			self.moves.append((0, -60 * (i+1)))

	def update_moves(self, all_pieces):
		self.move_rects = []
		for mov in self.moves:
			self.move_rects.append(pygame.Rect(self.piece_rect.x + mov[0], self.piece_rect.y + mov[1], 30, 30))

class King(Piece):
	def __init__(self, position, colour):
		super().__init__(position, colour)

		self.moves.append((60,0))
		self.moves.append((-60,0))
		self.moves.append((0,60))
		self.moves.append((0,-60))

	def update_moves(self, all_pieces):
		self.move_rects = []
		for mov in self.moves:
			self.move_rects.append(pygame.Rect(self.piece_rect.x + mov[0], self.piece_rect.y + mov[1], 30, 30))
