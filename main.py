import numpy
import pygame
import time

pygame.init()

# necessities
WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver")
FPS = 60
clock = pygame.time.Clock()

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (125, 125, 125)
BOX = (130, 130, 540, 540)

class Box:
    def __init__(self, row, col, width, total_rows, num):
        self.row = row - 2
        self.col = col - 2
        self.x = row * width + 130
        self.y = col * width + 130
        self.num = num
        self.width = width
        self.color = WHITE

    def change_num(self, new_num):
        self.num = new_num

    def draw_num(self, win, num):
        self.num_font = pygame.font.SysFont("calibri", 30)
        self.num_text = self.num_font.render(num, 1, BLACK)
        win.blit(self.num_text, (int(self.x + 30 - self.num_text.get_width()/2), int(self.y + 30 - self.num_text.get_height()/2)))

    def draw_color(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def is_selected(self):
        return self.color == RED

    def is_unselected(self):
        return self.color == WHITE

    def make_selected(self):
        self.color = RED

    def make_unselected(self):
        self.color = WHITE

    def make_empty(self):
        self.num = None

def make_grid(rows, width):
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            box = Box(i, j, gap, rows, None)
            grid[i].append(box)

    return grid

def draw_lines(win, rows, width):
    gap = width // rows
    for i in range(rows+1):
        # draw horizontal
        if i % 3 == 0 or i == 0:
            pygame.draw.line(WIN, BLACK, (130 + i * 60, 130), (130 + i * 60, 669), 5)
        else:
            pygame.draw.line(WIN, GREY, (130 + i * 60, 130), (130 + i * 60, 669), 1)
        for j in range(rows+1):
            # draw vertical
            if j % 3 == 0 or j == 0:
                pygame.draw.line(WIN, BLACK, (130, 130 + j * 60), (669, 130 + j * 60), 5)
            else:
                pygame.draw.line(WIN, GREY, (130, 130 + j * 60), (669, 130 + j * 60), 1)

def draw_reset(win):
    pygame.draw.rect(win, BLACK, (780, 130, 310, 180), 3)
    word_font = pygame.font.SysFont("calibri", 50)
    word_label = word_font.render("RESET", 1, BLACK)
    win.blit(word_label, (780 + int((310-word_label.get_width())/2), 130 + int((180-word_label.get_height())/2)))

def draw_solve(win):
    pygame.draw.rect(win, BLACK, (780, 490, 310, 180), 3)
    word_font = pygame.font.SysFont("calibri", 50)
    word_label = word_font.render("SOLVE", 1, BLACK)
    win.blit(word_label, (780 + int((310-word_label.get_width())/2), 490 + int((180-word_label.get_height())/2)))

def draw_header(win):
    word_font = pygame.font.SysFont("calibri", 50)
    word_label = word_font.render("SUDOKU SOLVER", 1, BLACK)
    win.blit(word_label, (int((WIDTH - word_label.get_width())/2), int((65 - word_label.get_height()/2))))

def draw(win, grid, rows, width, num):
    WIN.fill(WHITE)

    for row in grid:
        for box in row:
            num = box.num
            box.draw_color(win)
            box.draw_num(win, num)

    draw_lines(win, rows, width)
    draw_reset(win)
    draw_solve(win)
    draw_header(win)
    pygame.display.update()

def get_clicked_pos(pos, rows, cols, width, height):
    gap_x = width // cols
    gap_y = height // rows
    y, x = pos

    row = y // gap_y - 2
    col = x // gap_x - 2
    return row, col

def algorithm(grid):
    matrix = []

    for rows in grid:
        matrix.append([])

    # create matrix
    for rows in grid:
        for box in rows:
            matrix[rows.index(box)].append(box.num)

    #turn matrix strings into int and None into 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == None:
                matrix[i][j] = 0
            else:
                matrix[i][j] = int(matrix[i][j])

    return matrix

def solve(matrix):
    new_matrix = matrix
    for y in range(9):
        for x in range(9):
            if matrix[y][x] == 0:
                for n in range(1, 10):
                    if possible(y, x, n, matrix):
                        matrix[y][x] = n
                        solve(matrix)
                        if is_full(matrix):
                            return matrix
                        matrix[y][x] = 0
                return
    return new_matrix

def is_full(matrix):
    for x in range(0,9):
        for y in range(0, 9):
            if matrix[x][y] == 0:
                return False
    return True

def possible(y, x, n, matrix):
    for i in range(0, 9):
        if matrix[y][i] == n:
            return False
    for i in range(0, 9):
        if matrix[i][x] == n:
            return False
    x0 = (x//3) * 3
    y0 = (y//3) * 3
    for i in range(0, 3):
        for j in range(0, 3):
            if matrix[y0+i][x0+j] == n:
                return False
    return True

def not_in_row(matrix, row):

	# Set to store characters seen so far.
	st = set()

	for i in range(0, 9):

		# If already encountered before,
		# return false
		if matrix[row][i] in st:
			return False

		# If it is not an empty cell, insert value
		# at the current cell in the set
		if matrix[row][i] != 0:
			st.add(matrix[row][i])

	return True

# Checks whether there is any
# duplicate in current column or not.
def not_in_col(matrix, col):

	st = set()

	for i in range(0, 9):

		# If already encountered before,
		# return false
		if matrix[i][col] in st:
			return False

		# If it is not an empty cell, insert
		# value at the current cell in the set
		if matrix[i][col] != 0:
			st.add(matrix[i][col])

	return True

# Checks whether there is any duplicate
# in current 3x3 box or not.
def not_in_box(matrix, start_row, start_col):

	st = set()

	for row in range(0, 3):
		for col in range(0, 3):
			curr = matrix[row + start_row][col + start_col]

			# If already encountered before,
			# return false
			if curr in st:
				return False

			# If it is not an empty cell,
			# insert value at current cell in set
			if curr != 0:
				st.add(curr)

	return True

# Checks whether current row and current
# column and current 3x3 box is valid or not
def is_valid(matrix, row, col):

	return (not_in_row(matrix, row) and not_in_col(matrix, col) and
			not_in_box(matrix, row - row % 3, col - col % 3))


def is_valid_config(matrix):

	for i in range(0, 9):
		for j in range(0, 9):

			# If current row or current column or
			# current 3x3 box is not valid, return false
			if not is_valid(matrix, i, j):
				return False

	return True

def main(win, width, height):
    ROWS = 9
    COLS = 9
    grid = make_grid(ROWS, 540)

    run = True

    num = None

    while run:

        for row in grid:
            for box in row:
                pass

        clock.tick(FPS)

        draw(WIN, grid, ROWS, width, box.num)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # checks if mouse pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                coords = []
                for item in pos:
                    coords.append(item)

                # checking where on grid mouse press is
                row, col = get_clicked_pos(pos, ROWS, COLS, 540, 540)
                if row < 9 and col < 9 and row >= 0 and col >= 0:
                    box = grid[row][col]
                    if box.is_selected():
                        unselected = box
                        unselected.make_unselected()
                        time.sleep(0.05)
                    elif not box.is_selected():
                        selected = box
                        selected.make_selected()
                        time.sleep(0.05)

                # checking if reset button is pressed
                if 780 < coords[0] < 1090 and 130 < coords[1] < 310:
                    for row in grid:
                        for box in row:
                            box.change_num(None)

                elif 780 < coords[0] < 1090 and 490 < coords[1] < 670:
                    grid_state = algorithm(grid)
                    if is_valid_config(grid_state):

                        solution = solve(grid_state)

                        for a in range(9):
                            for b in range(9):
                                solution[a][b] = str(solution[a][b])

                        for i in range(9):
                            for j in range(9):
                                grid[j][i].change_num(solution[i][j])

            #checks if a number is pressed and will change square if box is selected
            if event.type == pygame.KEYDOWN:
                new_num = event.unicode
                if new_num.isdigit() and new_num != "0":
                    for row in grid:
                        for box in row:
                            if box.is_selected():
                                box.change_num(new_num)
                                box.make_unselected()
                                grid_state = algorithm(grid)

                # checks if BACKSPACE is pressed to clear a box
                elif event.key == pygame.K_BACKSPACE:
                    for row in grid:
                        for box in row:
                            if box.is_selected():
                                box.make_empty()

                # solves if SPACE key is pressed
                elif event.key == pygame.K_SPACE:
                    if is_valid_config(grid_state):
                        grid_state = algorithm(grid)

                        solution = solve(grid_state)
                        for a in range(9):
                            for b in range(9):
                                solution[a][b] = str(solution[a][b])

                        for i in range(9):
                            for j in range(9):
                                grid[j][i].change_num(solution[i][j])

    pygame.quit()

main(WIN, WIDTH, HEIGHT)
