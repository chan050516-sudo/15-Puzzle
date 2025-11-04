import random
import tkinter as tk

class Logic:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.board = [[None for _ in range(self.column)] for _ in range(self.row)]
        self.answer = [[None for _ in range(self.column)] for _ in range(self.row)]
        self.move_count = 0
        self.status = "Waiting to start"
    
    def set_board(self):
        for r in range(self.row):
            for c in range(self.column):
                self.answer[r][c] = (r*self.column) + (c+1)
                if self.answer[r][c] == 16:
                    self.answer[r][c] = " "
                self.board[r][c] = self.answer[r][c]
        return self.answer, self.board
        
    def move(self, clicked_r, clicked_c):
        dr = [-1, 1, 0, 0]
        dc = [0, 0, -1, 1]
        for i in range(len(dr)):
            nei_r = clicked_r + dr[i]
            nei_c = clicked_c + dc[i]
            if 0<=nei_r<self.row and 0<=nei_c<self.column:
                if self.board[nei_r][nei_c] == " ":
                    self.exchange(clicked_r, clicked_c, nei_r, nei_c)
                    self.move_count += 1
        return self.board, self.move_count
        
    def exchange(self, r1, c1, r2, c2):
        a = self.board[r1][c1]
        b = self.board[r2][c2]
        self.board[r1][c1] = b
        self.board[r2][c2] = a
        
    def shuffle(self):
        count=0
        blank_r, blank_c = self.row-1, self.column-1
        while count<=150:
            dr = [-1, 1, 0, 0]
            dc = [0, 0, -1, 1]
            i = random.randrange(len(dr))
            blanknei_r, blanknei_c = blank_r + dr[i], blank_c + dc[i]
            if 0<=blanknei_r<self.row and 0<=blanknei_c<self.column:
                self.exchange(blank_r, blank_c, blanknei_r, blanknei_c)
                blank_r, blank_c = blanknei_r, blanknei_c
                count += 1
                
    def check_status(self):
        if self.board == self.answer:
            self.status = "Done"
            
            
class UI():
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.root = tk.Tk()
        self.logic = Logic(self.row, self.column)
        self.puzzle = [[None for _ in range(self.column)] for _ in range(self.row)]
        self.status_tab = tk.Label(self.root, text="Waiting to start...")
        self.status_tab.grid(row=self.row+1, column=0, columnspan=self.column, rowspan =2)
        self.timer = tk.Label(self.root, text="0.0 s", bg = "grey")
        self.timer.grid(row=0, column=self.column-1, columnspan=2)
        self.time = 0
        self.start = tk.Button(self.root, text="Start", bg = "light yellow", command=self.on_click_start)
        self.start.grid(row=0, column=0, columnspan=2)
        self.disabled = True
    
    def all_disabled(self):
        if self.disabled:
            for row in range(self.row):
                for column in range(self.column):
                    self.puzzle[row][column].config(state = "disabled")
        else:
            for row in range(self.row):
                for column in range(self.column):
                    self.puzzle[row][column].config(state = "normal")
    
    def set_puzzle(self):
        self.logic.set_board()
        for row in range(self.row):
            for column in range(self.column):
                puzzle_button = tk.Button(self.root, text=str(self.logic.answer[row][column]), bg = "brown", width=1, command=lambda row=row, column=column: self.on_click_puzzle(row, column))
                puzzle_button.grid(row=row+1, column=column)
                self.puzzle[row][column] = puzzle_button
        self.all_disabled()
        return self.puzzle
    
    def on_click_start(self):
        self.logic.shuffle()
        self.updateui_puzzle()
        self.disabled = False
        self.all_disabled()
        self.logic.status = "In progress"
        self.start.config(text="Restart", bg="red")
        self.time = 0

    def on_click_puzzle(self, row, column):
        if self.logic.status == "Done":
            self.disabled = True
            self.all_disabled()
        else:
            self.logic.move(row, column)
            self.updateui_puzzle()
            self.logic.check_status()
            self.updateui_status_tab()
        
    def updateui_puzzle(self):
        for row in range(self.row):
            for column in range(self.column):
                self.puzzle[row][column].config(text=str(self.logic.board[row][column]))
                
    def updateui_status_tab(self):
        if self.logic.status == "Waiting to start":
            self.status_tab.config(text = "Waiting to start...")
        elif self.logic.status == "In progress":
            self.status_tab.config(text = f"Move Count: {self.logic.move_count}")
        elif self.logic.status == "Done":
            self.status_tab.config(text = f"Puzzle is completed!\nMove Count: {self.logic.move_count}")
            
    def updateui_timer(self):
        if self.logic.status == "In progress":
            self.time += 1
            self.timer.config(text = f"{self.time/10} s")
        self.root.after(100, self.updateui_timer)

if __name__ == "__main__":
    game1 = UI(4, 4)
    game1.set_puzzle()
    game1.updateui_timer()
    game1.root.mainloop()
