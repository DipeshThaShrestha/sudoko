from tkinter import *

root = Tk()
root.geometry('275x283')

# Solve the Sudoku
class SolveSudoku:
    def __init__(self):
        self.allZero()
        self.startSolution()

    # Set the empty cells to '0' (as strings for StringVar)
    def allZero(self):
        for i in range(9):
            for j in range(9):
                if savedNumbers[i][j].get() not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    savedNumbers[i][j].set('0')

    # Start the solving algorithm
    def startSolution(self, i=0, j=0):
        i, j = self.findNextCellToFill(i, j)

        # If i == -1, the Sudoku is solved or valid
        if i == -1:
            return True

        for e in range(1, 10):
            if self.isValid(i, j, e):
                savedNumbers[i][j].set(str(e))  # Set the value as a string for StringVar
                if self.startSolution(i, j):
                    return True
                # Undo the current cell for backtracking
                savedNumbers[i][j].set('0')
        return False

    # Find the nearest cell that needs to be filled
    def findNextCellToFill(self, i, j):
        for x in range(i, 9):
            for y in range(j, 9):
                if savedNumbers[x][y].get() == '0':
                    return x, y

        for x in range(0, 9):
            for y in range(0, 9):
                if savedNumbers[x][y].get() == '0':
                    return x, y

        return -1, -1

    # Check if placing 'e' in savedNumbers[i][j] is valid
    def isValid(self, i, j, e):
        # Check row
        for x in range(9):
            if savedNumbers[i][x].get() == str(e):
                return False
        # Check column
        for x in range(9):
            if savedNumbers[x][j].get() == str(e):
                return False

        # Check 3x3 subgrid
        secTopX, secTopY = 3 * (i // 3), 3 * (j // 3)
        for x in range(secTopX, secTopX + 3):
            for y in range(secTopY, secTopY + 3):
                if savedNumbers[x][y].get() == str(e):
                    return False
        return True

# GUI and frontend
class Launch:
    def __init__(self, master):
        self.master = master
        master.title("Sudoku Solver")

        font = ('Arial', 18)
        color = 'white'

        # Create the 9x9 grid for Sudoku
        self.__table = []
        for i in range(9):
            row = []
            for j in range(9):
                if (i < 3 or i > 5) and (j < 3 or j > 5) or (3 <= i <= 5 and 3 <= j <= 5):
                    color = 'light gray'
                else:
                    color = 'white'

                entry = Entry(master, width=2, font=font, bg=color, cursor='arrow', borderwidth=0,
                              highlightcolor='red', highlightthickness=1.2, highlightbackground='blue',
                              textvar=savedNumbers[i][j])
                entry.bind('<Motion>', self.correctGrid)
                entry.bind('<FocusIn>', self.correctGrid)
                entry.bind('<Button-1>', self.correctGrid)
                entry.grid(row=i, column=j)
                row.append(entry)
            self.__table.append(row)

        # Create Menu
        menu = Menu(master)
        master.config(menu=menu)

        file = Menu(menu)
        menu.add_cascade(label='File', menu=file)
        file.add_command(label='Solve', command=self.solveInput)
        file.add_command(label='Clear', command=self.clearAll)
        file.add_command(label='Exit', command=master.quit)

    # Correct grid if incorrect input
    def correctGrid(self, event):
        for i in range(9):
            for j in range(9):
                if savedNumbers[i][j].get() == '':
                    continue
                if len(savedNumbers[i][j].get()) > 1 or savedNumbers[i][j].get() not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    savedNumbers[i][j].set('')

    # Clear all cells
    def clearAll(self):
        for i in range(9):
            for j in range(9):
                savedNumbers[i][j].set('')

    # Call the solver
    def solveInput(self):
        solution = SolveSudoku()

# Initialize the savedNumbers matrix to store the numbers (as StringVar objects)
savedNumbers = [[StringVar(root) for _ in range(9)] for _ in range(9)]

# Launch the app
app = Launch(root)
root.mainloop()
