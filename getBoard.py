from typing import cast
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
    castleBlack = 'kq'
    castleWhite = 'KQ'
    #castling = 'KQkq'
    castleMap = {'a1' : True, 'e1' : True, 'h1' : True, 'h8' : True, 'e8' : True, 'a8' : True}

    def getBoard(self, driver, castling, white):
        # gets the board, draws that and calculate the best move and does it 
        self.clearBoardList()
        options = {
        "black rook" : 'r', "black knight" : 'n', "black bishop" : 'b', "black queen" : 'q', "black king" : 'k', "black pawn" : 'p', "white rook" : 'R', "white knight" : 'N', "white bishop" : 'B', "white queen" : 'Q', "white king" : 'K', "white pawn" : 'P'
        }
        pieces = driver.find_elements_by_tag_name('piece')
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
        #print(self.castleWhite + "    " + self.castleBlack)
        boardString = self.boardListToString(white, castling)
        return boardString

    def boardListToString(self, white, castling):
        boardString = ''
        newList = []
        for b in self.boardAsList:
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
            if self.boardAsList.index(b) != 7:
                s += '/'
            newList.append(s)

        for n in newList: boardString += n
        if white == True: move = 'w'
        else: 
            move = 'b'
            boardString = boardString[::-1]
        boardString += ' ' + move
        boardString += ' ' + str(castling)
        return boardString

    def checkCastle(self, driver, nextMove, castleList):
        # check if already castled
        moveList = driver.find_elements_by_tag_name('u8t')
        for move in moveList:
            # check if already castled 
            if move.text == 'O-O-O' or move.text == 'O-O':
                i = moveList.index(move)
                if (i+1) % 2 == 0:
                    castleList[2] = ""
                    castleList[3] = ""
                else: 
                    print('here 2')
                    castleList[0] = ""
                    castleList[1] = ""

        # check if rock has moves
        if nextMove[:2] == 'a1':
            castleList[1] = ''
        if nextMove[:2] == 'h1':
            castleList[0] = ''
        if nextMove[:2] == 'a8':
            castleList[3] = ''
        if nextMove[:2] == 'h8':
            castleList[2] = ''
        # check if king moves 
        if nextMove[:2] == 'e1':
            castleList[1] = ''
            castleList[2] = ''
        if nextMove[:2] == 'e8':
            castleList[1] = ''
            castleList[2] = ''
        return castleList

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