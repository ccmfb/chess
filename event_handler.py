import settings
import pygame

class Event_Handler:

	def check_events(self, all_pieces):

		# Check events
		for event in pygame.event.get():

			# Quit
			if event.type == pygame.QUIT:
					settings.running = False

			# Check each piece
			if event.type == pygame.MOUSEBUTTONDOWN:
				for colou in all_pieces:
					for typ in colou:	
						for piece in typ:
							self.check_moving(event, piece, all_pieces)
							self.check_moves(event, piece, all_pieces)

	# Check whether to move piece or not
	def check_moving(self, event, piece, all_pieces):

		# Only move piece if piece is showing its possible moves
		if piece.showing_moves:

			# Check if one of the possible moves is clicked
			for rect in piece.move_rects:
				if rect.collidepoint(event.pos):
					piece.move(all_pieces, rect.x, rect.y)

	# Check whether to show possible moves of piece or not
	def check_moves(self, event, piece, all_pieces):

		# Check whether to set showing moves to true
		if piece.piece_rect.collidepoint(event.pos):
			piece.update_moves(all_pieces)
			piece.showing_moves = True
		else:
			piece.showing_moves = False







