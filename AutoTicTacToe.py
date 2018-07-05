'''
    
    TicTacToe Game System vs. Player
    using Min Max Algorithm
    Graphical User Interface Implemented in Python Tk
'''
from Tkinter import Tk, Label, Frame, Canvas, Button, ALL

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

class TTT:
    '''
        main class for interface and game handling
    '''
    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.pack(fill="both", expand=True)
        self.label = Label(self.frame, text='Tic Tac Toe Game', height=2, font="Arial 14", bg='black', fg='blue')
        self.label.pack(fill="both", expand=True)
        self.canvas = Canvas(self.frame, width=300, height=300)
        self.canvas.pack(fill="both", expand=True)
        self.status = Label(self.frame, text='Start Game', height=2, font="Arial 14", bg='white', fg='black')
        self.status.pack(fill="both", expand=True)
        self.reset = Button(self.frame, text="Reset Game", command=self.reset)
        self.reset.pack(fill="both", expand=True)
        self.__board()
        self.canvas.bind("<ButtonPress-1>", self.handler)
        self.board = [0 for x in range(0, 9)]
        self.winner = None
        self.lastmoves = []

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

    def __board(self):
        self.canvas.create_rectangle(0, 0, 300, 300, outline="black")
        self.canvas.create_rectangle(100, 300, 200, 0, outline="black")
        self.canvas.create_rectangle(0, 100, 300, 200, outline="black")

    def reset(self):
        self.canvas.delete(ALL)
        self.__board()
        self.changeStatus('Start Game')
        self.canvas.bind("<ButtonPress-1>", self.handler)
        self.board = [0 for x in range(0, 9)]
        self.winner = None
        self.lastmoves = []

    def changeStatus(self, status):
        self.status['text'] = status

    def markFinal(self, pos, marker):
        x = pos%3
        y = int(pos/3)
        # print pos, marker
        if marker == 2:
            X = 100 * (x + 1)
            Y = 100 * (y + 1)
            self.canvas.create_oval(X - 25, Y - 25, X - 75, Y - 75, width=4, outline="green")
            self.changeStatus("X's Move !")
        else:
            X = 100 * x
            Y = 100 * y
            self.canvas.create_line(X + 25, Y + 25, X + 75, Y + 75, width=4, fill="red")
            self.canvas.create_line(X + 25, Y + 75, X + 75, Y + 25, width=4, fill="red")
            self.changeStatus("O's Move !")
        
        self.board[pos] = marker

    def handler(self, event):
        '''
        handle mouse click event on the board
        '''
        x = int(event.x / 100)
        y = int(event.y / 100)
        if self.board[y*3+x] == 0:
            self.markFinal(y*3+x, 2)
            if self.is_gameover():
                self.canvas.unbind("<ButtonPress-1>")
                if self.winner == 2:
                    self.changeStatus("O Won the Game !")
                elif self.winner == 1:
                    self.changeStatus("X Won the Game !")
                else:
                    self.changeStatus("Game Draw !")
                return

            pos, score = min_max_move(self, 1)
            self.markFinal(pos, 1);

            if self.is_gameover():
                self.canvas.unbind("<ButtonPress-1>")
                if self.winner == 2:
                    self.changeStatus("O Won the Game !")
                elif self.winner == 1:
                    self.changeStatus("X Won the Game !")
                else:
                    self.changeStatus("Game Draw !") 

# Program Starts Here
root = Tk()
app = TTT(root)
root.mainloop()
