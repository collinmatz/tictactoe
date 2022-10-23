'''
a class to hold the board and board functions
'''
class Board:
    def __init__(self, w=3, h=3):
        self.w = w
        self.h = h
        self.board = [([-1] * w) for _ in range(h)]
    
    def reset(self):
        '''
        reset the board to be all empty values
        '''
        self.board = [([-1] * self.w) for _ in range(self.h)]