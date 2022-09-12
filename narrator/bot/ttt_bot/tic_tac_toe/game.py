from ast import Tuple
import random


class TicTacToeGame:
    """
    Tic-tac-toe Game
    """

    def __init__(self) -> None:
        self._board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self._winner = 0
        self._fields_left = 9
        self._player = 1

    def _check_win(self, i, j) -> int:
        if self._board[i][0] == self._board[i][1] == self._board[i][2] != 0:
            return self._board[i][j]
        if self._board[0][j] == self._board[1][j] == self._board[2][j] != 0:
            return self._board[i][j]
        if self._board[0][0] == self._board[1][1] == self._board[2][2] != 0:
            return self._board[i][j]
        if self._board[0][2] == self._board[1][1] == self._board[2][0] != 0:
            return self._board[i][j]
        return 0

    def move_manually(self, i, j):
        if self._board[i][j] != 0:
            raise IndexError("Illegal move")
        self._board[i][j] = self._player
        self._fields_left -= 1
        self._winner = self._check_win(i, j)
        self._player = 3 - self._player

    def move_ai(self):
        rival = 3 - self._player
        player = self._player
        for i in range(3):
            for j in range(3):
                if self._board[i][j] == 0:
                    self._board[i][j] = player
                    if self._check_win(i, j) == player:
                        self._board[i][j] = 0
                        self.move_manually(i, j)
                        return
                    self._board[i][j] = 0

        for i in range(3):
            for j in range(3):
                if self._board[i][j] == 0:
                    self._board[i][j] = rival
                    if self._check_win(i, j) == rival:
                        self._board[i][j] = 0
                        self.move_manually(i, j)
                        return
                    self._board[i][j] = 0
        g0 = [[1, 1]]
        g1 = [[0, 0], [2, 2], [0, 2], [2, 0]]
        random.shuffle(g1)
        g2 = [[1, 0], [1, 2], [0, 1], [2, 1]]
        random.shuffle(g2)

        for i, j in g0 + g1 + g2:
            if self._board[i][j] == 0:
                self.move_manually(i, j)
                return

    @property
    def status(self) -> Tuple(str, int):
        if self._winner:
            return ("Win", self._winner)
        elif self._fields_left == 0:
            return ("Tie", 0)
        else:
            return ("Ongoing", 0)
