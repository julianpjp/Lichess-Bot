import time
from getBoard import GetBoard
from chessEngine import Chess
from move import Move

class Listener():

    movesDone = 0
    castleList = ['K', 'Q', 'k', 'q']

    def __init__(self, driver, timePerMove, white):
        self.white = white
        self.driver = driver
        self.timePerMove = timePerMove
        self.listener()
    
    def listener(self): 
        # listener to check if you have to move
        while True:
            movesCount = len(self.driver.find_elements_by_tag_name('u8t'))
            if self.white == True:
                if movesCount % 2 == 0:
                    if movesCount != 0 or self.movesDone < movesCount:
                        print('white and move!')
                        self.getBestMove()
            else:
                if movesCount % 2 != 0:
                    #print('!= 0')
                    if self.movesDone < movesCount:
                        print('black and move!')
                        self.getBestMove()
            time.sleep(2.5)

    def getBestMove(self):
        #self.movesDone = movesCount 
        boardString = GetBoard().getBoard(self.driver, self.ListToString(self.castleList), self.white)
        nextMove = Chess().getNextMove(boardString, self.timePerMove)
        self.castleList = GetBoard().checkCastle(self.driver, str(nextMove.move), self.castleList)
        print(self.castleList)
        print('next move' + str(nextMove))
        Move().doMove(self.driver, nextMove)
        return

    def ListToString(self, castleList):
        s = ''
        for e in castleList:
            s += str(e)
        return s