# 1028 Python Game
# Import a library of functions called 'pygame'
import pygame
from board import Board
from solver import Solver
 
def main():
	# Initialize the game engine
	pygame.init()

	# Set the height and width of the screen
	tileSize = 100
	size = (100+4*tileSize, 100+4*tileSize)
	screen = pygame.display.set_mode(size)
	gameBoard = Board(tileSize, screen)
	gameSolver = Solver(gameBoard) 
	 
	pygame.display.set_caption("Jeremy's 2048 Game")
	 
	# Loop until the user clicks the close button.
	done = False
	gameStart = False
	clock = pygame.time.Clock()

	# Clear the screen and set the screen background
	screen.fill(gameBoard.COLORDICT[2])

	# Loop as long as done == False
	while not done:

	    for event in pygame.event.get():  # User did something
	        if event.type == pygame.QUIT:  # If user clicked close
	            done = True  # Flag that we are done so we exit this loop

	        if pygame.key.get_focused():
		        keys = pygame.key.get_pressed()

		        if not gameStart:
		        	if keys[pygame.K_SPACE]:
			        	gameBoard.beginGame()
			        	gameStart = True
		        else:
		        	if keys[pygame.K_i] and gameBoard.upPossible(gameBoard.boardMatrix):
		        		gameBoard.move(0,gameBoard.boardMatrix, gameBoard.prevboardMatrix)
		        		# gameBoard.getNewTile(gameBoard.boardMatrix)

		        	elif keys[pygame.K_k] and gameBoard.downPossible(gameBoard.boardMatrix):
		        		gameBoard.move(1,gameBoard.boardMatrix, gameBoard.prevboardMatrix)
		        		# gameBoard.getNewTile(gameBoard.boardMatrix)

		        	elif keys[pygame.K_j] and gameBoard.leftPossible(gameBoard.boardMatrix):
		        		gameBoard.move(2,gameBoard.boardMatrix, gameBoard.prevboardMatrix)
		        		# gameBoard.getNewTile(gameBoard.boardMatrix)

		        	elif keys[pygame.K_l] and gameBoard.rightPossible(gameBoard.boardMatrix):
		        		gameBoard.move(3,gameBoard.boardMatrix, gameBoard.prevboardMatrix)
		        		# gameBoard.getNewTile(gameBoard.boardMatrix)

		        	elif keys[pygame.K_u]:
		        		gameBoard.numOfMoves -= 1
		        		gameBoard.printMatrix(gameBoard.prevboardMatrix)
		        		gameBoard.refreshBoard(gameBoard.prevboardMatrix)
		        		gameBoard.boardMatrix[:] = gameBoard.prevboardMatrix[:]

		        	elif keys[pygame.K_s]:
		        		gameSolver.solve()

		        	if gameBoard.isFull():
		        		if gameBoard.upPossible(gameBoard.boardMatrix):
		        			pass
		        		elif gameBoard.downPossible(gameBoard.boardMatrix):
		        			pass
		        		elif gameBoard.rightPossible(gameBoard.boardMatrix):
		        			pass
		        		elif gameBoard.leftPossible(gameBoard.boardMatrix):
		        			pass
		        		else:
		        			gameStart = False
		        			gameBoard.gameOver()
	 
	    # All drawing code happens after the for loop and but
	    # inside the main while not done loop.
	 
	    # Go ahead and update the screen with what we've drawn.
	    # This MUST happen after all the other drawing commands.
	    pygame.display.flip()
	 
	    # This limits the while loop to a max of 60 times per second.
	    # Leave this out and we will use all CPU we can.
	    clock.tick(60)
	 
	# Be IDLE friendly
	pygame.quit()

if __name__ == "__main__":
    main()