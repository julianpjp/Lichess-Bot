from time import time
from typing import cast
import chess.engine


class Chess():

    engine = chess.engine.SimpleEngine.popen_uci("stockfish_20090216_x64_avx2.exe")

    def getNextMove(self, boardString, timeLimit):
        self.drawBoard(boardString)
        board = chess.Board(boardString)
        #if board.is_check():
        #   return 'check'
        limit = chess.engine.Limit(time=timeLimit)
        return self.engine.play(board, limit)  

    def drawBoard(self, boardString):
        board = chess.Board(boardString)
        print(board)

