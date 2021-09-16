import pygame
import operator

WHITE_PIECES = (220,220,220)
BLACK_PIECES = (192,192,192)

class Piece:
	def __init__(self, position, colour):
		self.showing_moves = False
		
		# Teams
		self.colour = colour
		self.colour_rgb = WHITE_PIECES if self.colour == 'w' else BLACK_PIECES

		# Different rectangles for moves etc.
		self.piece_rect = pygame.Rect(position[0] - 15, position[1] - 15, 30, 30)
		self.moves = []
		self.move_rects = []
		self.beat_rects = []

		self.font = pygame.font.SysFont('Helvetica Neue', 15)

	def update_moves(self, all_pieces):
		
		# Clear moves
		self.move_rects = []
		self.beat_rects = []

		# Only append moves which are inside the board boundaries
		for mov_type in self.moves:						
			for mov in mov_type:

				# Check for board boundaries
				if 0 < self.piece_rect.x + mov[0] < 480:
					if 0 < self.piece_rect.y + mov[1] < 480:
						self.move_rects.append(pygame.Rect(self.piece_rect.x + mov[0], self.piece_rect.y + mov[1], 30, 30))

		# Remove blocked spaces
		for mov_type in self.moves:
			for mov in mov_type:
				for team in all_pieces:
					for type_of_piece in team:
						for piece in type_of_piece:
							
							# Check for other pieces blocking the way
							self.check_blocks(piece, mov)

	def check_blocks(self, piece, mov):
		if self.colour == 'w':

			# When other piece is whtie (same team) remove every further move and the move where piece is
			if piece.colour == 'w':
				if self.piece_rect.x + mov[0] == piece.piece_rect.x and self.piece_rect.y + mov[1] == piece.piece_rect.y:
					if piece.piece_rect in self.move_rects:
						self.move_rects.remove(piece.piece_rect)
						self.remove_further_moves(mov)

			# When other piece is in opposing team, add option to defeat enemy piece
			if piece.colour == 'b':
				if self.piece_rect.x + mov[0] == piece.piece_rect.x and self.piece_rect.y + mov[1] == piece.piece_rect.y:
					if piece.piece_rect in self.move_rects:
						self.move_rects.append(pygame.Rect(self.piece_rect.x + mov[0], self.piece_rect.y + mov[1], 30, 30))
						self.beat_rects.append(pygame.Rect(self.piece_rect.x + mov[0] - 10, self.piece_rect.y + mov[1] - 10, 50, 50))
						self.remove_further_moves(mov)

		if self.colour == 'b':

			# When other piece is black (same team) remove every further move and the move where piece is
			if piece.colour == 'b':
				if self.piece_rect.x + mov[0] == piece.piece_rect.x and self.piece_rect.y + mov[1] == piece.piece_rect.y:
					if piece.piece_rect in self.move_rects:
						self.move_rects.remove(piece.piece_rect)
						self.remove_further_moves(mov)

			# When other piece is in opposing team, add option to defeat enemy piece
			if piece.colour == 'w':
				if self.piece_rect.x + mov[0] == piece.piece_rect.x and self.piece_rect.y + mov[1] == piece.piece_rect.y:
					if piece.piece_rect in self.move_rects:
						self.move_rects.append(pygame.Rect(self.piece_rect.x + mov[0], self.piece_rect.y + mov[1], 30, 30))
						self.beat_rects.append(pygame.Rect(self.piece_rect.x + mov[0] - 10, self.piece_rect.y + mov[1] - 10, 50, 50))
						self.remove_further_moves(mov)

	def remove_further_moves(self, move):
		to_delete_moves = []

		# Check which move type to truncate
		for mov_type in self.moves:
			if move in mov_type:

				# truncate move type based on position of block
				to_delete_moves = mov_type[mov_type.index(move):]

		# Delete further moves
		for mov in to_delete_moves:
			if pygame.Rect(self.piece_rect.x + mov[0], self.piece_rect.y + mov[1], 30, 30) in self.move_rects:
				self.move_rects.remove(pygame.Rect(self.piece_rect.x + mov[0], self.piece_rect.y + mov[1], 30, 30))

	def move(self, all_pieces, to_x, to_y):	
		self.piece_rect.x = to_x
		self.piece_rect.y = to_y

		self.defeat_piece(all_pieces)

	def defeat_piece(self, all_pieces):
		
		# Check for other piece
		if self.colour == 'w':
			for other_type in all_pieces[1]:
				for other_piece in other_type:
					
					# Remove piece if it collides with moved piece
					if self.piece_rect.x == other_piece.piece_rect.x and self.piece_rect.y == other_piece.piece_rect.y:
						all_pieces[1][all_pieces[1].index(other_type)].remove(other_piece)
		
		if self.colour == 'b':
			for other_type in all_pieces[0]:
				for other_piece in other_type:
					
					# Remove piece if it collides with moved piece
					if self.piece_rect.x == other_piece.piece_rect.x and self.piece_rect.y == other_piece.piece_rect.y:
						all_pieces[0][all_pieces[0].index(other_type)].remove(other_piece)

		
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
		
		# 4 Possible ways of movement (normal, start pos, 2 * beating enemy)
		self.moves = [[],[],[],[]]

		# Adding possible moves
		if colour == 'w':
			self.moves[0].append((0,60))
			self.moves[1].append((0,120))
			self.moves[2].append((-60, 60))
			self.moves[3].append((60, 60))
		elif colour == 'b':
			self.moves[0].append((0,-60))
			self.moves[1].append((0,-120))
			self.moves[2].append((-60, -60))
			self.moves[3].append((60, -60))

		self.textsurf = self.font.render('P', False, (0,179,255))

	def update_moves(self, all_pieces):
		super().update_moves(all_pieces)

		# Remove start position move when not on start position
		if self.colour == 'w':
			if self.piece_rect.y != 75:
				if pygame.Rect(self.piece_rect.x + self.moves[1][0][0], self.piece_rect.y + self.moves[1][0][1], 30, 30) in self.move_rects:
					self.move_rects.remove(pygame.Rect(self.piece_rect.x + self.moves[1][0][0], self.piece_rect.y + self.moves[1][0][1], 30, 30))
		elif self.colour == 'b':
			if self.piece_rect.y != 375:
				if pygame.Rect(self.piece_rect.x + self.moves[1][0][0], self.piece_rect.y + self.moves[1][0][1], 30, 30) in self.move_rects:
					self.move_rects.remove(pygame.Rect(self.piece_rect.x + self.moves[1][0][0], self.piece_rect.y + self.moves[1][0][1], 30, 30))

		# Remove left-defeat if there doesnt exist an opponent
		if pygame.Rect(self.piece_rect.x + self.moves[2][0][0] - 10, self.piece_rect.y + self.moves[2][0][1] - 10, 50, 50) not in self.beat_rects:
			if pygame.Rect(self.piece_rect.x + self.moves[2][0][0], self.piece_rect.y + self.moves[2][0][1], 30, 30) in self.move_rects:
				self.move_rects.remove(pygame.Rect(self.piece_rect.x + self.moves[2][0][0], self.piece_rect.y + self.moves[2][0][1], 30, 30))

		# Remove right-defeat if there doesnt exist an opponent
		if pygame.Rect(self.piece_rect.x + self.moves[3][0][0] - 10, self.piece_rect.y + self.moves[3][0][1] - 10, 50, 50) not in self.beat_rects:
			if pygame.Rect(self.piece_rect.x + self.moves[3][0][0], self.piece_rect.y + self.moves[3][0][1], 30, 30) in self.move_rects:
				self.move_rects.remove(pygame.Rect(self.piece_rect.x + self.moves[3][0][0], self.piece_rect.y + self.moves[3][0][1], 30, 30))

		# Remove defeat rect that is (0,2) away
		if pygame.Rect(self.piece_rect.x + self.moves[1][0][0] - 10, self.piece_rect.y + self.moves[1][0][1] - 10, 50, 50) in self.beat_rects:
			self.beat_rects.remove(pygame.Rect(self.piece_rect.x + self.moves[1][0][0] - 10, self.piece_rect.y + self.moves[1][0][1] - 10, 50, 50))

		# Remove forwards move if there is an opponent in front
		if pygame.Rect(self.piece_rect.x + self.moves[0][0][0] - 10, self.piece_rect.y + self.moves[0][0][1] - 10, 50, 50) in self.beat_rects:
			if pygame.Rect(self.piece_rect.x + self.moves[0][0][0], self.piece_rect.y + self.moves[0][0][1], 30, 30) in self.move_rects:
				self.move_rects.remove(pygame.Rect(self.piece_rect.x + self.moves[0][0][0], self.piece_rect.y + self.moves[0][0][1], 30, 30))

		# Remove forward defeat if there is an opponent in front
		if pygame.Rect(self.piece_rect.x + self.moves[0][0][0] - 10, self.piece_rect.y + self.moves[0][0][1] - 10, 50, 50) in self.beat_rects:
			self.beat_rects.remove(pygame.Rect(self.piece_rect.x + self.moves[0][0][0] - 10, self.piece_rect.y + self.moves[0][0][1] - 10, 50, 50))

class Rock(Piece):
	def __init__(self, position, colour):
		super().__init__(position, colour)

		# 4 Possible types of movement
		self.moves = [[],[],[],[]]

		for i in range(7):
			self.moves[0].append((60 * (i+1), 0))
			self.moves[1].append((-60 * (i+1), 0))
			self.moves[2].append((0, 60 * (i+1)))
			self.moves[3].append((0, -60 * (i+1)))

		self.textsurf = self.font.render('R', False, (0,179,255))

class Knight(Piece):
	def __init__(self, position, colour):
		super().__init__(position, colour)

		# 8 Possible types of movement
		self.moves = [[],[],[],[],[],[],[],[]]

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

		# 4 Possible types of movement
		self.moves = [[],[],[],[]]

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
		self.moves = [[],[],[],[],[],[],[],[]]

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
		self.moves = [[],[],[],[],[],[],[],[]]

		self.moves[0].append((60,0))
		self.moves[1].append((-60,0))
		self.moves[2].append((0,60))
		self.moves[3].append((0,-60))

		self.moves[4].append((60,60))
		self.moves[5].append((-60,60))
		self.moves[6].append((60,-60))
		self.moves[7].append((-60,-60))

		self.textsurf = self.font.render('Ki', False, (0,179,255))

