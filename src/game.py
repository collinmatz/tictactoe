from board import Board
from bot import Bot

'''
class to control the main game components
'''
class Game:
    def __init__(self, diff):
        self.board = Board()
        self.bot = Bot(diff)
    
    def determineVictory(self):
        '''
        checks all possible victory positions and returns true
        if there is a victory
        '''
        b = self.board.board
        if (
            (b[0][0] != -1 and (b[0][0] == b[0][1] == b[0][2])) or
            (b[1][0] != -1 and (b[1][0] == b[1][1] == b[1][2])) or
            (b[2][0] != -1 and (b[2][0] == b[2][1] == b[2][2])) or
            (b[0][0] != -1 and (b[0][0] == b[1][0] == b[2][0])) or
            (b[0][1] != -1 and (b[0][1] == b[1][1] == b[2][1])) or
            (b[0][2] != -1 and (b[0][2] == b[1][2] == b[2][2])) or
            (b[0][0] != -1 and (b[0][0] == b[1][1] == b[2][2])) or
            (b[0][2] != -1 and (b[0][2] == b[1][1] == b[2][0]))
        ):
            return True
        else:
            return False

    def reset(self):
        '''
        reset the board to all empty values
        '''
        self.board.reset()

    def updateBoard(self, pos, state):
        '''
        update a single position of the board
        '''
        self.board.board[pos[0]][pos[1]] = state

    def spaceAvailable(self, pos):
        '''
        check to see if a current position is currently available
        '''
        return self.board.board[pos[0]][pos[1]] == -1
        
    def AITurn(self):
        '''
        determine the best place to go for the AI
        '''
        return self.bot.getNextMove(self.board.board)
        

