from tkinter import *
from game import Game
from random import randint
from config import Config

'''
the main class for the application. houses the GUI components, as well as
interfaces to the game class in order to dispatch commands across the components
'''
class TicTacToe:
    def __init__(self):
        # initialize the gui and set the geometry
        self.root = Tk()
        self.root.geometry('300x350')
        self.root.resizable(False, False)
        self.root.title(f'Tic-Tac-Toe AI V{Config.version}')

        # initialize the game canvas for the shapes and text
        self.canvas = Canvas(self.root)
        self.canvas.bind('<Button-1>', self.handleClick)

        # store the bounds for each square. Stored in the format:
        #   [ (low_x, lo_y) , (hi_x, hi_y) ] 
        # for each cell
        self.bounds = [
            [[(20,20),(105,105)],[(108,20),(192,105)],[(195,20),(280,105)]],
            [[(20,108),(105,192)],[(107,107),(193,193)],[(195,108),(280,192)]],
            [[(20,195),(105,280)],[(108,195),(192,280)],[(195,195),(280,280)]]
        ]

        # store the game shapes and shape parameters
        self.shapes = []
        offset = Config.shapeSize if Config.shapeSize <= 40 and Config.shapeSize >= 0 else 20
        self.shapeOffset = 50 - Config.shapeSize # adjusts the size of the shapes

        # possible colors can be hex or lowercase strings
        self.playerColor = Config.playerColor
        self.botColor = Config.botColor

        # draw board
        vLine1 = self.canvas.create_line(105,20,105,280)
        vLine2 = self.canvas.create_line(195,20,195,280)
        hLine1 = self.canvas.create_line(20,105,280,105)
        hLine2 = self.canvas.create_line(20,195,280,195)
        # box = self.canvas.create_rectangle(20,20,280,280)

        self.text = Label(self.root, text='Your Turn.')
        self.text.pack()

        # stats tracking
        self.playerWins = 0
        self.AIWins = 0
        self.draws = 0
        self.winsText = Label(self.root, text=f'Player Wins: {self.playerWins}  AI Wins: {self.AIWins}  Draws: {self.draws}')
        self.winsText.pack()

        # pack board
        self.canvas.pack(expand=1, fill=BOTH)

        # bot difficulty
        useDepth = False
        diff = -1
        if Config.botDifficulty > -1:
            useDepth = True
            diff = int(Config.botDifficulty)

        # game object
        self.game = Game(diff)
        self.starter = 0
        self.totalTurns = 0
        self.useDepth = False

    def reset(self):
        '''
        reset the game board and delete all the drawn shapes
        '''
        for shape in self.shapes:
            self.canvas.delete(shape)
        self.text.configure(text='Your Turn.')
        self.shapes = []
        self.game.reset()
        self.totalTurns = 0

        self.starter = 1 if self.starter == 0 else 0

        if self.starter == 1:
            self.AITurn(random=True)
    
    def handleClick(self, event):
        '''
        handles when a player clicks the screen. need to determine what
        square the player is clicking based on the coordiantes stored
        in event.x and event.y
        '''
        # column 1
        if event.x > 20 and event.x < 105:
            if event.y > 20 and event.y < 105:
                self.updateBoard([0,0])
            elif event.y > 105 and event.y < 195:
                self.updateBoard([1,0])
            elif event.y > 195 and event.y < 280:
                self.updateBoard([2,0])
        # column 2
        elif event.x > 105 and event.x < 195:
            if event.y > 20 and event.y < 105:
                self.updateBoard([0,1])
            elif event.y > 105 and event.y < 195:
                self.updateBoard([1,1])
            elif event.y > 195 and event.y < 280:
                self.updateBoard([2,1])
        # column 3
        elif event.x > 195 and event.x < 280:
            if event.y > 20 and event.y < 105:
                self.updateBoard([0,2])
            elif event.y > 105 and event.y < 195:
                self.updateBoard([1,2])
            elif event.y > 195 and event.y < 280:
                self.updateBoard([2,2])
    
    def updateBoard(self, pos):
        '''
        draw a shape in the specified cell. check the game
        board first for an already occupied cell
        '''
        if not self.game.spaceAvailable([pos[0], pos[1]]):
            print('Square already occupied')
            return

        bounds = self.bounds[pos[0]][pos[1]]
        lowBoundsX = bounds[0][0] + self.shapeOffset
        lowBoundsY = bounds[0][1] + self.shapeOffset
        hiBoundsX = bounds[1][0] - self.shapeOffset
        hiBoundsY = bounds[1][1] - self.shapeOffset

        newShape = self.canvas.create_oval(lowBoundsX, lowBoundsY, hiBoundsX, hiBoundsY, outline=self.playerColor)

        self.shapes.append(newShape)
        self.game.updateBoard([pos[0], pos[1]], 0)
        self.totalTurns += 1
        self.root.after(10, lambda: self.determineWin(0))
        self.text.configure(text='AI Moving...')
    
    def determineWin(self, turn):
        '''
        determine if there has been a victory
        '''
        if self.game.determineVictory():
            if turn == 0:
                self.text.configure(text='Player wins!')
                self.playerWins += 1
            else:
                self.text.configure(text='AI Wins!')
                self.AIWins += 1
            self.winsText.configure(text=f'Player Wins: {self.playerWins}  AI Wins: {self.AIWins}  Draws: {self.draws}')
            self.root.after(1000, self.reset)
        elif self.totalTurns > 8:
            self.text.configure(text='Draw!')
            self.draws += 1
            self.winsText.configure(text=f'Player Wins: {self.playerWins}  AI Wins: {self.AIWins}  Draws: {self.draws}')
            self.root.after(1000, self.reset)
        else:
            if turn == 0:
                self.root.after(1000, self.AITurn)
    
    def AITurn(self, random=False):
        '''
        run the AI turn sequence. The AI searches through its
        state space of all possible moves and returns the
        move that gives the greatest chance of winning
        '''
        # AI turn : get the best position using minimax
        self.text.configure(text='AI Moving...')
        pos = None
        if random:
            pos = (randint(0,2), randint(0,2))
        else:
            pos = self.game.AITurn()

        bounds = self.bounds[pos[0]][pos[1]]
        lowBoundsX = bounds[0][0] + self.shapeOffset
        lowBoundsY = bounds[0][1] + self.shapeOffset
        hiBoundsX = bounds[1][0] - self.shapeOffset
        hiBoundsY = bounds[1][1] - self.shapeOffset

        self.game.updateBoard([pos[0], pos[1]], 1)
        newShape = self.canvas.create_rectangle(lowBoundsX, lowBoundsY, hiBoundsX, hiBoundsY, outline=self.botColor)
        self.shapes.append(newShape)

        self.root.after(10, lambda: self.determineWin(1))
        self.text.configure(text='Your Turn.')
        self.totalTurns += 1

if __name__ == '__main__':
    game = TicTacToe()
    game.root.mainloop()