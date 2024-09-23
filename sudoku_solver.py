import tkinter as tk
from tkinter import messagebox
from typing import List, Tuple, Optional

# Constants
GRID_SIZE = 9
SUBGRID_SIZE = 3
EMPTY_CELL = 0

class SudokuSolver:
    @staticmethod
    def solve(board: List[List[int]]) -> bool:
        empty = SudokuSolver.find_empty(board)
        if not empty:
            return True
        row, col = empty

        for num in range(1, GRID_SIZE + 1):
            if SudokuSolver.is_valid(board, num, (row, col)):
                board[row][col] = num

                if SudokuSolver.solve(board):
                    return True

                board[row][col] = EMPTY_CELL

        return False

    @staticmethod
    def find_empty(board: List[List[int]]) -> Optional[Tuple[int, int]]:
        return next(((i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if board[i][j] == EMPTY_CELL), None)

    @staticmethod
    def is_valid(board: List[List[int]], num: int, pos: Tuple[int, int]) -> bool:
        row, col = pos

        # Check row and column
        if num in board[row] or num in (board[i][col] for i in range(GRID_SIZE)):
            return False

        # Check 3x3 box
        box_x, box_y = col // SUBGRID_SIZE, row // SUBGRID_SIZE
        for i in range(box_y * SUBGRID_SIZE, box_y * SUBGRID_SIZE + SUBGRID_SIZE):
            for j in range(box_x * SUBGRID_SIZE, box_x * SUBGRID_SIZE + SUBGRID_SIZE):
                if board[i][j] == num and (i, j) != pos:
                    return False

        return True

class SudokuGUI:
    def __init__(self, master: tk.Tk):
        self.master = master
        self.master.title("Sudoku Solver")
        self.board = [[EMPTY_CELL for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.cells = {}

        self.create_grid()
        self.create_buttons()

    def create_grid(self):
        outer_frame = tk.Frame(self.master, bd=3, relief=tk.RAISED)
        outer_frame.grid(row=0, column=0, padx=10, pady=10)

        for i in range(SUBGRID_SIZE):
            for j in range(SUBGRID_SIZE):
                inner_frame = tk.Frame(outer_frame, bd=1, relief=tk.SUNKEN)
                inner_frame.grid(row=i, column=j, padx=2, pady=2)
                self.fill_3x3_grid(inner_frame, i, j)

    def fill_3x3_grid(self, frame: tk.Frame, outer_row: int, outer_col: int):
        for i in range(SUBGRID_SIZE):
            for j in range(SUBGRID_SIZE):
                row, col = outer_row * SUBGRID_SIZE + i, outer_col * SUBGRID_SIZE + j
                cell_entry = tk.Entry(frame, width=3, justify="center", font=("Arial", 20))
                cell_entry.grid(row=i, column=j, padx=1, pady=1, ipady=5)
                self.cells[(row, col)] = cell_entry

    def create_buttons(self):
        button_frame = tk.Frame(self.master)
        button_frame.grid(row=1, column=0, pady=10, sticky="ew")
        button_frame.columnconfigure((0, 1, 2), weight=1)

        button_height = 2

        buttons = [
            ("Solve", self.solve),
            ("Clear", self.clear),
            ("Quit", self.master.quit)
        ]

        for col, (text, command) in enumerate(buttons):
            tk.Button(button_frame, text=text, command=command, height=button_height).grid(
                row=0, column=col, padx=5, sticky="nsew"
            )

        self.master.columnconfigure(0, weight=1)
        button_frame.rowconfigure(0, weight=1)

    def solve(self):
        self.board = self.get_board()
        if SudokuSolver.solve(self.board):
            self.update_gui()
        else:
            messagebox.showerror("Error", "No solution exists")

    def clear(self):
        for cell in self.cells.values():
            cell.delete(0, tk.END)

    def get_board(self) -> List[List[int]]:
        return [[int(self.cells[(i, j)].get()) if self.cells[(i, j)].get().isdigit() else EMPTY_CELL
                 for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]

    def update_gui(self):
        for (i, j), cell in self.cells.items():
            cell.delete(0, tk.END)
            cell.insert(0, str(self.board[i][j]))

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    SudokuGUI(root)
    root.mainloop()
