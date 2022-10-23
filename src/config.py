'''
a class to store application configurations.
any simple modifications can be made here!

*note: if you change the color and are getting an error when you attempt to
play, you might have inputted your color incorrectly
'''
class Config:
    version = 1.0
    playerColor = 'lime'
    botColor = 'red'
    shapeSize = 1

    # bot difficulty : the difficulty corresponds to the number of moves the AI is able to
    #   see ahead. If it is -1, the bot will be able to see an infinite number of moves ahead
    botDifficulty = -1