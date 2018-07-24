#!/usr/bin/env python3

class TicTacToe:
    def __init__(self):
        self.grid = [[' ']*3 for i in range(3)]
        self.player = 'X'

    def start(self):
        while self.turn():
            pass
        print("This game is over.")

    # Check if current player has won
    def winner(self):
        for i in range(3):
            if self.player == self.grid[i][0] == self.grid[i][1] == self.grid[i][2]:
                print("Player", self.player, "has won!")
                return True
            if self.player == self.grid[0][i] == self.grid[1][i] == self.grid[2][i]:
                print("Player", self.player, "has won!")
                return True

        if self.player == self.grid[0][0] == self.grid[1][1] == self.grid[2][2]:
            print("Player", self.player, "has won!")
            return True
        if self.player == self.grid[2][0] == self.grid[1][1] == self.grid[0][2]:
            print("Player", self.player, "has won!")
            return True

        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == ' ':
                    return False
        print("There was a tie! Nobody wins!")
        return True

    def paint(self):
        print ("It is", self.player + "'s turn.")
        print(' | '.join(self.grid[0]))
        print('---------')
        print(' | '.join(self.grid[1]))
        print('---------')
        print(' | '.join(self.grid[2]))

    # Returns True if another turn is needed
    def turn(self):
        self.paint()
        coords = self.get_coords()
        while coords == False:
            print("Please enter a pair of coords from 0-2 (ex. 1 1).")
            print("The coords must point to an empty space.")
            coords = self.get_coords()
        x, y = coords[0], coords[1]
        self.grid[y][x] = self.player
        if self.winner():
            return False
        if self.player == 'X':
            self.player = 'O'
        else:
            self.player = 'X'
        return True

    def get_coords(self):
        coords = input().split(" ")
        if len(coords) != 2:
            return False
        try:
            x = int(coords[0])
            y = int(coords[1])
            if (x < 0 or x > 2):
                return False
            if (y < 0 or y > 2):
                return False
            if self.grid[y][x] != ' ':
                return False
            return (x, y)
        except (ValueError, TypeError):
            return False


if __name__ == '__main__':
    game = TicTacToe();
    game.start()
