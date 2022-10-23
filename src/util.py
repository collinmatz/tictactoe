player = 0
bot = 1

def evaluate(board):
    '''
    calculate the current score of the board depending on who is closer to win.
    If the player is closer to a win, return a maximum score (10). If the AI is closer
    to a win, return a minimum score (-10).

    to calculate these scores, just check each possible victory position
    '''
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2]:
            if board[row][0] == player:
                return 10
            elif board[row][0] == bot:
                return -10

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col]:
            if board[0][col] == player:
                return 10
            elif board[0][col] == bot:
                return -10

    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == player:
            return 10
        elif board[0][0] == bot:
            return -10

    if board[0][2] == board[1][1] == board[2][0]:
        if board[0][2] == player:
            return 10
        elif board[0][2] == bot:
            return -10

    return 0

def isMovesLeft(board):
    '''
    checks to see if there are possible moves left
    '''
    for i in range(3):
        for j in range(3):
            if board[i][j] == -1:
                return True
    return False

def minimax(board, useDepth, isMaximizingPlayer, depth):
    '''
    recursively check each board state for a winning
    position. The minimizer is trying to minimize the maximizer's
    next move, while the maximizer is trying to maximize its own move

    TODO: implement alpha-beta pruning
    '''
    score = evaluate(board)
    if useDepth and depth <= 0:
        return 0

    if score == 10 or score == -10:
        return score

    if not isMovesLeft(board):
        return 0

    if isMaximizingPlayer:
        bestVal = -1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == -1:
                    board[i][j] = player
                    bestVal = max(bestVal, minimax(board, useDepth, not isMaximizingPlayer, depth-1))
                    board[i][j] = -1
        return bestVal

    else:
        bestVal = 1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == -1:
                    board[i][j] = bot
                    bestVal = min(bestVal, minimax(board, useDepth, not isMaximizingPlayer, depth-1))
                    board[i][j] = -1
        return bestVal


if __name__ == '__main__':
    # unit testing for the util functions.
    # set the board to be a predefined state and run the util.py file
    #   to see expected results from the bot's best move function

    board = [
        [1,0,1],
        [0,0,1],
        [0,-1,0]
    ]

    bestVal = 1000
    bestMove = (-1,-1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == -1:
                board[i][j] = bot
                moveVal = minimax(board, 0, True)
                board[i][j] = -1
                if moveVal < bestVal:
                    bestVal = moveVal
                    bestMove = (i,j)
    
    print(bestMove)