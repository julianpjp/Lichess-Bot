import re
from chessEngine import Chess
from selenium import webdriver
import time

class Move():

    drag = [None] * 2
    droop =[None] * 2
    fields = { 'a' : 8, 'b' : 7, 'c' : 6, 'd' : 5, 'e' : 4, 'f' : 3, 'g' : 2, 'h' : 1 }
    moveDone = False

    def doMove(self, driver, nextMove):
        self.driver = driver
        if nextMove.resigned == True:
            self.resign()
            return

        board = self.driver.find_element_by_tag_name('cg-board')
        self.getPosition(nextMove.move, board)
        print(str(self.drag), "   ", str(self.droop))    

        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element_with_offset(board, self.drag[0], self.drag[1])
        action.click()
        action.perform()
        time.sleep(0.2)
        
        action.reset_actions
        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element_with_offset(board, self.droop[0], self.droop[1])
        action.click()
        action.perform()
        
        """
        boardAsList2 = GetBoard().getBoard()
        if boardAsList1 != boardAsList2:
            self.moveDone = True
        else:
            self.moveDone = False 
        return self.moveDone
        """
        
    def getPosition(self, move, board):
        moveList = [*str(move)]
        boardLength = board.size['width']
        squareLength = boardLength / 8
        print(boardLength)
        print(moveList)
        self.drag[0] = int(squareLength * self.fields.get(moveList[0])) - (squareLength / 2)
        self.drag[1] = int(squareLength * int(moveList[1])) - (squareLength / 2)
        self.droop[0] = int(squareLength * self.fields.get(moveList[2])) - (squareLength / 2)
        self.droop[1] = int(squareLength * int(moveList[3])) - (squareLength / 2)
        return

    def showMove(self):
        return

    def resign(self):
        print('resign!')
        resignButton = self.driver.find_element_by_class('fbt resign')
        resignButton.click()
        return

#boardlist = ['RNBKQBNR', 'PPPP1PPP', '11111111', '1111P111', '11111111', '11111111', 'pppppppp', 'rnbkqbnr']
#c = Chess().getNextMove(boardlist, 2.0, "KQkq", True)
#Move().doMove(c, 10)