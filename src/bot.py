from util import minimax

'''
a class to control the AI for the game
'''
class Bot:
    def __init__(self, diff=5, turn=1):
        self.turn = turn
        self.useDepth = True if diff > -1 else False
        self.diff = diff

    def getNextMove(self, board):
        '''
        finds the next best move for the AI to take.
        The AI is the minimizer in this case, trying to
        minimize the player's chance of winning.
        '''
        bestVal = 1000
        bestMove = (-1,-1)

        for i in range(3):
            for j in range(3):
                if board[i][j] == -1:
                    board[i][j] = self.turn
                    moveVal = minimax(board, useDepth=self.useDepth, isMaximizingPlayer=True, depth=self.diff)
                    board[i][j] = -1
                    if moveVal < bestVal:
                        bestVal = moveVal
                        bestMove = (i,j)

        return bestMove

