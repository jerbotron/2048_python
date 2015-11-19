# board.py
import pygame
from random import *

class Board(object):
	def __init__(self, tileSize, screen):
		self.tile_size = tileSize
		self.screen = screen
		self.boardMatrix = [0] * 16
		self.prevboardMatrix = [0] * 16
		self.numOfMoves = 0

		# Colors:
		self.COLORDICT = {
			'BLACK': (0, 0, 0),
			'WHITE': (255, 255, 255),
			'FRAME': (187, 173, 160) ,
			2: (238, 228, 218),
			4: (237, 224, 200),
			8: (242, 117, 121),
			16: (245, 149, 99),
			32: (246, 124, 95),
			64: (246, 94, 59),
			128: (237, 207, 114),
			256: (237, 204, 97),
			512: (237, 200, 80),
			1024: (237, 200, 80),
			2048: (237, 200, 80)
		}

	def drawTiles(self):
	    # Draw board tiles 4x4
	    for x in range(0,4):
	    	for y in range(0,4):
	    		pygame.draw.rect(self.screen, self.COLORDICT['FRAME'], [50+x*self.tile_size, 50+y*self.tile_size, self.tile_size, self.tile_size], 2)

	def refreshTiles(self, boardMatrix, x, y):
		num = boardMatrix[x+4*y]
		font_size = 54

		if (num < 10):
			x_cord = 88+x*self.tile_size
			y_cord = 75+y*self.tile_size
		elif (num < 100):
			x_cord = 75+x*self.tile_size
			y_cord = 75+y*self.tile_size
		elif (num < 1000):
			x_cord = 62+x*self.tile_size
			y_cord = 75+y*self.tile_size
		else:
			font_size = 34
			x_cord = 67+x*self.tile_size
			y_cord = 84+y*self.tile_size

		color = self.COLORDICT[num]
		numberFont = pygame.font.SysFont('Calibri', font_size, True, False)
		text = numberFont.render(str(boardMatrix[x + 4 * y]),True, self.COLORDICT['WHITE'])
		pygame.draw.rect(self.screen, color, [52+x*self.tile_size, 52+y*self.tile_size, self.tile_size-4, self.tile_size-4], 0)
		self.screen.blit(text, [x_cord, y_cord])

	def refreshBoard(self, boardMatrix):
		# Clear the screen and set the screen background
		self.screen.fill(self.COLORDICT[2])
		movesStr = "Number of Moves: " + str(self.numOfMoves)
		movesCounter = pygame.font.SysFont('Calibri', 16, True).render(movesStr,True,self.COLORDICT['BLACK'])
		self.screen.blit(movesCounter, (50,25))
		self.drawTiles();
		for x in range(0,4):
			for y in range(0,4):
				if (boardMatrix[x + 4 * y] != 0):
					self.refreshTiles(boardMatrix,x,y)

	def beginGame(self):
		self.drawTiles()

		while True:
			p1 = randint(0,15)
			p2 = randint(0,15)
			if (p1 != p2):
				self.boardMatrix[p1] = randint(1,2)*2
				self.boardMatrix[p2] = randint(1,2)*2
				break

		self.refreshBoard(self.boardMatrix)

	def gameOver(self):
		self.boardMatrix = [0] * 16
		self.numOfMoves = 0
		s = pygame.Surface((500,500))
		s.set_alpha(95)

		pygame.draw.rect(s, self.COLORDICT[2], [0,0,500,500])
		text1 = pygame.font.SysFont('Calibri', 32, True).render("GAME OVER",True,self.COLORDICT['BLACK'])
		text2 = pygame.font.SysFont('Calibri', 16, True).render("PRESS SPACEBAR TO CONTINUE...",True,self.COLORDICT['BLACK'])
		self.screen.blit(s,(0,0))
		self.screen.blit(text1,(170, 200))
		self.screen.blit(text2,(140, 245))
		print "Game Over!"

	def move(self, direction, boardMatrix, prevboardMatrix = None):
		# 0 = up, 1 = down, 2 = left, 3 = right
		temp = boardMatrix[:]

		# print "================================================="
		# print("Before move:")
		# self.printMatrix(boardMatrix)

		# print("Prev boardMatrix:")
		# self.printMatrix(prevboardMatrix)

		"""
		Stack Algorithm:
		1) First collapse all zeros with first non-zero number in respective row/column
		2) Then check for next available non-zero number
		3) Check if they can be added up, replace old tiles with 0's
		4) Repeat until all tiles have been checked
		"""

		if (direction == 0):
			# print("Up")
			for x in range(0,4):
				for y in range(0,3):
					count = 0
					while boardMatrix[x+4*y] == 0:
						for i in range(y,3):
							boardMatrix[x+4*i] = boardMatrix[x+4*(i+1)]
							boardMatrix[x+4*(i+1)] = 0
						if count == 4 - y: break
						count+=1
						
					j = y + 1

					while (boardMatrix[x+4*j] == 0 and j < 3):
						j+=1

					if (boardMatrix[x+4*y] == boardMatrix[x+4*j]):
						boardMatrix[x+4*y] += boardMatrix[x+4*j]
						boardMatrix[x+4*j] = 0
		elif(direction == 1):
			# print("Down")
			for x in range(0,4):
				for y in range(3,0,-1):
					count = 0
					while boardMatrix[x+4*y] == 0:
						for i in range(y,0,-1):
							boardMatrix[x+4*i] = boardMatrix[x+4*(i-1)]
							boardMatrix[x+4*(i-1)] = 0
						if count == y - 1: break
						count+=1
						
					j = y - 1

					while (boardMatrix[x+4*j] == 0 and j > 0):
						j-=1

					if (boardMatrix[x+4*y] == boardMatrix[x+4*j]):
						boardMatrix[x+4*y] += boardMatrix[x+4*j]
						boardMatrix[x+4*j] = 0
		elif (direction == 2):
			# print("Left")
			for y in range(0,4):
				for x in range(0,3):
					count = 0
					while boardMatrix[x+4*y] == 0:
						for i in range(x,3):
							boardMatrix[i+4*y] = boardMatrix[(i+1)+4*y]
							boardMatrix[(i+1)+4*y] = 0
						if count == 4 - x: break
						count+=1
						
					j = x + 1

					while (boardMatrix[j+4*y] == 0 and j < 3):
						j+=1

					if (boardMatrix[x+4*y] == boardMatrix[j+4*y]):
						boardMatrix[x+4*y] += boardMatrix[j+4*y]
						boardMatrix[j+4*y] = 0
		elif (direction == 3):
			# print("Right")
			for y in range(0,4):
				for x in range(3,0,-1):
					count = 0
					while boardMatrix[x+4*y] == 0:
						for i in range(x,0,-1):
							boardMatrix[i+4*y] = boardMatrix[(i-1)+4*y]
							boardMatrix[(i-1)+4*y] = 0
						if count == x - 1: break
						count+=1
							
					j = x - 1

					while (boardMatrix[j+4*y] == 0 and j > 0):
						j-=1

					if (boardMatrix[x+4*y] == boardMatrix[j+4*y]):
						boardMatrix[x+4*y] += boardMatrix[j+4*y]
						boardMatrix[j+4*y] = 0

		# print("After move:")
		# self.printMatrix(boardMatrix)

		if (temp != boardMatrix and prevboardMatrix != None):
			# print "Actual move"
			self.numOfMoves += 1
			prevboardMatrix[:] = temp[:]
			self.getNewTile(boardMatrix)
			# print("Added new tile:")
			# self.printMatrix(boardMatrix)

		# print("Prev boardMatrix:")
		# self.printMatrix(prevboardMatrix)

	def getNewTile(self, boardMatrix):
		count = 0
		for i in range(len(self.boardMatrix)):
			if (self.boardMatrix[i] == 0):
				count+=1

		if count == 0:
			return

		# print "count = " + str(count)

		new_pos = randint(1,count)
		new_val = randint(1,2)*2

		# print "new_pos = " + str(new_pos)
		# print "new_val = " + str(new_val)

		n = 0

		for i in range(len(self.boardMatrix)):
			if self.boardMatrix[i] == 0:
				n+=1
			if n == new_pos:
				self.boardMatrix[i] = new_val
				break

		self.refreshBoard(boardMatrix)
		print("Added new tile:")
		self.printMatrix(boardMatrix)

	def printMatrix(self, boardMatrix):
		for y in range(0,4):
			print(boardMatrix[4*y:4*(y+1)])

	def isFull(self):
		for i in self.boardMatrix:
			if i == 0:
				return False
		return True

	def upPossible(self, boardMatrix):
		temp = boardMatrix[:]
		self.move(0, temp)
		if temp == boardMatrix:
			return False
		else:
			return True

	def downPossible(self, boardMatrix):
		temp = boardMatrix[:]
		self.move(1, temp)
		if temp == boardMatrix:
			return False
		else:
			return True

	def leftPossible(self, boardMatrix):
		temp = boardMatrix[:]
		self.move(2, temp)
		if temp == boardMatrix:
			return False
		else:
			return True

	def rightPossible(self, boardMatrix):
		temp = boardMatrix[:]
		self.move(3, temp)
		if temp == boardMatrix:
			return False
		else:
			return True