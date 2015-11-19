# board.py
import pygame
from board import Board
from random import *


class Solver(object):
	def __init__(self, gameBoard):
		self.gameBoard = gameBoard
		self.biggest = 2
		self.smallest = 2
		self.solverOn = True

	def refreshScreen(self):
		pygame.display.flip()
		pygame.time.wait(300)

	'''
	Main AI Solver Function
	'''
	def solve(self):
		# print self.findBestMove(self.gameBoard.boardMatrix)
		while self.solverOn:
			if self.checkMaxCorner() == False:
				self.buildMaxCorner()
			elif self.checkRowFull(0) == False:
				self.buildTopRow()
			elif self.rowCollapsible(0) == True:
				self.collapseTopRow()
			else:
				if (self.solverOn == False):
					break
				else:
					self.populateBoard()

	'''
	Gameboard Mover Functions
	'''
	def buildTopRow(self):
		# Ensure top row is all non-zero
		if self.gameBoard.upPossible(self.gameBoard.boardMatrix):
			self.gameBoard.move(0, self.gameBoard.boardMatrix, self.gameBoard.prevboardMatrix)
			self.refreshScreen()
		elif self.gameBoard.leftPossible(self.gameBoard.boardMatrix):
			self.gameBoard.move(2, self.gameBoard.boardMatrix, self.gameBoard.prevboardMatrix)
			self.refreshScreen()
		elif self.gameBoard.rightPossible(self.gameBoard.boardMatrix):
			self.gameBoard.move(3, self.gameBoard.boardMatrix, self.gameBoard.prevboardMatrix)
			self.refreshScreen()

	def collapseTopRow(self):
		# Move left on top row
		self.gameBoard.move(2, self.gameBoard.boardMatrix, self.gameBoard.prevboardMatrix)
		self.refreshScreen()

	def populateBoard(self):
		if self.gameBoard.rightPossible(self.gameBoard.boardMatrix):
			# Move right on board
			self.gameBoard.move(3, self.gameBoard.boardMatrix, self.gameBoard.prevboardMatrix)
			self.refreshScreen()
		elif self.gameBoard.leftPossible(self.gameBoard.boardMatrix):
			# Move left on board
			self.gameBoard.move(2, self.gameBoard.boardMatrix, self.gameBoard.prevboardMatrix)
			self.refreshScreen()
		elif self.gameBoard.upPossible(self.gameBoard.boardMatrix):
			# Move up on board
			self.gameBoard.move(0, self.gameBoard.boardMatrix, self.gameBoard.prevboardMatrix)
			self.refreshScreen()
		else:
			print "Turn solver off"
			self.solverOn = False

	def buildMaxCorner(self):
		big = self.getBiggest(self.gameBoard.boardMatrix)
		corner = self.gameBoard.boardMatrix[0]
		if self.checkRowEmpty(0):
			# Move Up
			self.gameBoard.move(0, self.gameBoard.boardMatrix, self.gameBoard.prevboardMatrix)
			self.refreshScreen()
		elif big < 4 and self.maxShiftLeft():
			# Move Left
			self.gameBoard.move(2, self.gameBoard.boardMatrix, self.gameBoard.prevboardMatrix)
			self.refreshScreen()
		else:
			move = self.findBestMove(self.gameBoard.boardMatrix)
			self.gameBoard.move(move, self.gameBoard.boardMatrix, self.gameBoard.prevboardMatrix)
			self.refreshScreen()
			
	'''
	Gameboard Status Checking Functions
	'''
	def rowCollapsible(self, row):
		for i in range(3):
			if self.gameBoard.boardMatrix[4*row+i] != 0 and self.gameBoard.boardMatrix[4*row+i] == self.gameBoard.boardMatrix[4*row+i+1]:
				return True
		return False

	def checkRowFull(self, row):
		for i in range(4):
			if self.gameBoard.boardMatrix[4*row+i] == 0:
				return False
		return True

	def checkRowEmpty(self, row):
		for i in range(4):
			if self.gameBoard.boardMatrix[4*row+i] != 0:
				return False
		return True

	def checkMaxCorner(self):
		if self.getBiggest(self.gameBoard.boardMatrix) != 0:
			return False
		return True

	def maxShiftLeft(self):
		big = self.getBiggest(self.gameBoard.boardMatrix)
		# Assuming biggest number is in first row
		for i in range(big-1,-1,-1):
			if self.gameBoard.boardMatrix[i] != 0:
				return False
		return True

	def findBestMove(self, boardMatrix):
		upVal = 0
		leftVal = 0
		if self.gameBoard.upPossible(boardMatrix):
			temp = boardMatrix[:]
			self.gameBoard.move(0,temp)
			upVal = temp[0]

		# if boardMatrix.downPossible():
		# 	temp = boardMatrix[:]
		# 	self.gameBoard.move(1,temp)
		# 	downVal = temp[0]

		if self.gameBoard.leftPossible(boardMatrix):
			temp = boardMatrix[:]
			self.gameBoard.move(2,temp)
			leftVal = temp[0]

		# if boardMatrix.rightPossible():
		# 	temp = boardMatrix[:]
		# 	self.gameBoard.move(3,temp)
		# 	rightVal = temp[0]
		if upVal == 0 and leftVal == 0:
			return -1
		elif upVal > leftVal:
			return 0
		else:
			return 2

	def getBiggest(self, boardMatrix):
		temp = 2
		idx = 0
		for i in range(len(boardMatrix)):
			if boardMatrix[i] > temp:
				temp = boardMatrix[i]
				idx = i
		return idx

	def getSmallest(self, boardMatrix):
		temp = 0
		idx = 0
		for i in range(len(boardMatrix)):
			if boardMatrix[i] != 0:
				if temp == 0 or boardMatrix[i] < temp:
					temp = boardMatrix[i]
					idx = i			
		return idx