'''Automation of Game TicTacToe
 on android device Moto G3 for
 Game on Google play store (https://play.google.com/store/apps/details?id=com.pinkpointer.tictactoe)
 Environments
 Opencv for python
 adb tool for debugging

 '''
class Game:
    def __init__(self):
        self.board = [ 0 for i in range(0,9) ]
        # self.board = [1, 0, 0, 0, 1, 0, 2, 0, 0]
        self.lastmoves = []
        self.winner = None

    def get_free_cells(self):
        moves = []
        for i,v in enumerate(self.board):
            if v == 0:
                moves.append(i)
        return moves

    def mark(self,pos, marker):
        self.board[pos] = marker
        self.lastmoves.append(pos)

    def revert_last_move(self):
        self.board[self.lastmoves.pop()] = 0
        self.winner = None

    def is_gameover(self):
        win_positions = [(0,1,2), (3,4,5), (6,7,8), (0,3,6),(1,4,7),(2,5,8), (0,4,8), (2,4,6)]
        for i,j,k in win_positions:
            if self.board[i] == self.board[j] and self.board[j] == self.board[k] and self.board[i] != 0:
                self.winner = self.board[i]
                return True
        if 0 not in self.board:
            self.winner = 0
            return True
        return False
    def get_score(self):
    	if self.is_gameover():
    		if self.winner == 2:
    			return 1 # Won
    		elif self.winner == 1:
    			return -1
    	return 0
    def get_cell_value(self,pos):
        return self.board[pos]

    def is_moved(self):
        for cell in self.board:
            if cell != 0:
                return True
        return False
        
def min_max_move(instance, marker):
	bestmove = None
	bestscore = None
	
	if marker == 2:
		for m in instance.get_free_cells():
			instance.mark(m, 2)
			if instance.is_gameover():
				score = instance.get_score()
			else:
				mov_pos, score = min_max_move(instance, 1)
			instance.revert_last_move()

			if bestscore == None or score > bestscore:
				bestscore = score
				bestmove = m
	else:
		for m in instance.get_free_cells():
			instance.mark(m, 1)
			if instance.is_gameover():
				score = instance.get_score()
			else:
				mov_pos, score = min_max_move(instance, 2)
			instance.revert_last_move()

			if bestscore == None or score < bestscore:
				bestscore = score
				bestmove = m
	return bestmove, bestscore



positions = [(52, 513), (292, 513), (530, 513), (55, 757), (298, 757), (540, 757), (52, 992), (294, 992), (533, 992)]

import cv2
from os import system
from random import randint
from time import sleep

## Computer is 'X' <-> 2 and mobile is 'O' <-> 1

game = Game()

pos = randint(0,8)

system("adb shell screencap -p /sdcard/tictac.png")
system("adb pull /sdcard/tictac.png")
img = cv2.imread('tictac.png')

for i,v in enumerate(positions):
    if game.get_cell_value(i) == 0 and img[v[1]][v[0]][2] == 248:
        game.mark(i, 1)
    elif game.get_cell_value(i) == 0 and img[v[1]][v[0]][2] == 105:
        game.mark(i, 2)

if game.is_moved() == False:
    system("adb shell input tap "+str(positions[pos][0])+" "+str(positions[pos][1]))

for k in range(0,4):
    system("adb shell screencap -p /sdcard/tictac.png")
    system("adb pull /sdcard/tictac.png")
    img = cv2.imread('tictac.png')
    for i,v in enumerate(positions):
        if game.get_cell_value(i) == 0 and img[v[1]][v[0]][2] == 248:
            game.mark(i, 1)
        elif game.get_cell_value(i) == 0 and img[v[1]][v[0]][2] == 105:
            game.mark(i, 2)
    # print game.board
    pos, score = min_max_move(game, 2)
    system("adb shell input tap "+str(positions[pos][0])+" "+str(positions[pos][1]))
    if game.is_gameover():
        break
