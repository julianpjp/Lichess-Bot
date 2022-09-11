from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.common.by import By
from chessEngine import Chess
from move import Move
import asyncio
import re
import time

class GetBoard():

    squareLength = None
    boardAsList = []
    movesDone = 0
    castling = 'KQkq'
    castleMap = {'a1' : True, 'e1' : True, 'h1' : True, 'h8' : True, 'e8' : True, 'a8' : True}

    def __init__(self, driver, white, timePerMove):
        self.driver = driver
        self.white = white
        self.timePerMove = timePerMove

        self.listener()

    def getBoard(self):
        # gets the board, draws that and calculate the best move and does it 
        self.clearBoardList()
        options = {
        "black rook" : 'r', "black knight" : 'n', "black bishop" : 'b', "black queen" : 'q', "black king" : 'k', "black pawn" : 'p', "white rook" : 'R', "white knight" : 'N', "white bishop" : 'B', "white queen" : 'Q', "white king" : 'K', "white pawn" : 'P'
        }
        pieces = self.driver.find_elements_by_tag_name('piece')
        self.getSquareLength(pieces)
        for piece in pieces:
            c = piece.get_attribute("class")
            name = options.get(c)
            if (name != None):
                style = piece.get_attribute('style')
                #print(c + "    " + style)
                transform = self.getPositonOfPiece(style)
                line = self.boardAsList[transform[1]]
                lineList = list(line)
                lineList[transform[0]] = name
                line=''
                for l in lineList: line += l
                self.boardAsList[transform[1]] = line
        
    def boardListToString(self, boardList, castling, white):
        # converts the list of strings to an string in the FEN protocol and returns that
        boardString = ''
        newList = []
        for b in boardList:
            s = ''
            i = 0
            add = 0
            isOne = False
            oldList = list(b)
            for c in oldList:
                i += 1
                if c == '1':
                    isOne = True
                    add = add+1
                    if i == 8:
                        s += (str(add))
                else: 
                    if isOne == True:
                        s += (str(add))
                        add = 0
                        isOne = False
                    s += c
            if boardList.index(b) != 7:
                s += '/'
            newList.append(s)

        for n in newList: boardString += n
        if white == True: move = 'w'
        else: 
            move = 'b'
            boardString = boardString[::-1]
        boardString += ' ' + move
        boardString += ' ' + str(castling)
        print(boardString)
        return boardString
        
    def startMove(self):
        print(self.boardAsList)
        nextMove = Chess().getNextMove(self.boardAsList, self.timePerMove, self.castling, self.white)
        asyncio.run(self.checkCastling(nextMove))
        b = Move().doMove(self.driver, nextMove, self.boardAsList)
        return b

    async def checkCastling(self, nextMove):
        self.castling = ''
        move = str(nextMove.move)[:2]
        if move == 'e1':
            self.castleMap['a1'] = False
            self.castleMap['h1'] = False
        if move == 'e8':
            self.castleMap['a8'] = False
            self.castleMap['h8'] = False
        if move in self.castleMap:
            self.castleMap[move] = False

        if self.castleMap.get('h1') == True:
            self.castling += 'K'
        if self.castleMap.get('a1') == True:
            self.castling += 'Q'
        if self.castleMap.get('h8') == True:
            self.castling += 'k'#
        if self.castleMap.get('a8') == True:
            self.castling += 'q'
        
        print(nextMove)
        print(str(self.castleMap) + "    " + str(self.castling))
        print(self.boardAsList)
        return


    def listener(self): 
        # listener to check if you have to move
        while True:
            movesCount = len(self.driver.find_elements_by_tag_name('u8t'))
            move = False
            if self.white == True:
                if movesCount % 2 == 0:
                    if movesCount == 0 or self.movesDone < movesCount:
                        print('white and move!')
                        self.getBoard()
                        move = self.startMove()
            else:
                if movesCount % 2 != 0:
                    #print('!= 0')
                    if self.movesDone < movesCount:
                        print('black and move!')
                        self.getBoard()
                        move = self.startMove()
            if move == True:
                self.movesDone = movesCount 
            time.sleep(0.5)

    def getPositonOfPiece(self, style):
        a = re.findall(r'\d+', style)
        transform = []
        for t in a:
            transform.append(int(int(t) / self.squareLength))
        return transform

    def getSquareLength(self, pieces):
        # gets the length of one square
        if len(pieces) > 0:
            piece = pieces[0]
            self.squareLength = (piece.size).get('height')


    def clearBoardList(self):
        # clears the array and fills it with ones
        self.boardAsList.clear()
        empty = "11111111"
        for i in range(8):
            self.boardAsList.append(empty)
        return