import tkinter as tk
import random

# --- Konstanta ---
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 25
GAME_SPEED = 500  # Milidetik

# --- Warna ---
COLORS = {
    "I": "#00f0f0",
    "O": "#f0f000",
    "T": "#a000f0",
    "S": "#00f000",
    "Z": "#f00000",
    "J": "#0000f0",
    "L": "#f0a000",
}

# --- Bentuk Blok ---
SHAPES = {
    "I": [[".....", "..#..", "..#..", "..#..", "..#.."]],
    "O": [[".....", ".....", ".##..", ".##..", "....."]],
    "T": [[".....", ".....", ".#...", "###..", "....."]],
    "S": [[".....", ".....", ".##..", "##...", "....."]],
    "Z": [[".....", ".....", "##...", ".##..", "....."]],
    "J": [[".....", ".#...", ".#...", "##...", "....."]],
    "L": [[".....", "...#.", "...#.", "##...", "....."]],
}


class TetrisApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tetris (Tanpa Install)")
        self.resizable(False, False)

        # --- Variabel Game ---
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.get_new_piece()
        self.score = 0
        self.game_over = False

        # --- Buat UI ---
        self.create_widgets()

        # --- Mulai Game Loop ---
        self.game_loop()

    def create_widgets(self):
        # Frame Utama
        main_frame = tk.Frame(self, bg="black")
        main_frame.pack(padx=10, pady=10)

        # Canvas untuk menggambar game
        self.canvas = tk.Canvas(
            main_frame,
            width=GRID_WIDTH * CELL_SIZE,
            height=GRID_HEIGHT * CELL_SIZE,
            bg="black",
            highlightthickness=2,
            highlightbackground="white",
        )
        self.canvas.pack(side=tk.LEFT)

        # Panel Info
        info_frame = tk.Frame(main_frame, bg="black", width=150)
        info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))

        tk.Label(
            info_frame,
            text="TETRIS",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="black",
        ).pack(pady=(0, 20))

        self.score_label = tk.Label(
            info_frame,
            text=f"Score: {self.score}",
            font=("Arial", 14),
            fg="white",
            bg="black",
        )
        self.score_label.pack(pady=5)

        tk.Label(
            info_frame,
            text="Controls:",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="black",
        ).pack(pady=(20, 5))
        tk.Label(
            info_frame, text="← → : Move", font=("Arial", 10), fg="gray", bg="black"
        ).pack()
        tk.Label(
            info_frame, text="↓ : Soft Drop", font=("Arial", 10), fg="gray", bg="black"
        ).pack()
        tk.Label(
            info_frame, text="↑ : Rotate", font=("Arial", 10), fg="gray", bg="black"
        ).pack()

        # Bind Keyboard
        self.bind("<Left>", lambda e: self.move(-1, 0))
        self.bind("<Right>", lambda e: self.move(1, 0))
        self.bind("<Down>", lambda e: self.move(0, 1))
        self.bind("<Up>", lambda e: self.rotate())
        self.focus_set()

    def get_new_piece(self):
        shape_key = random.choice(list(SHAPES.keys()))
        return {
            "shape": SHAPES[shape_key],
            "color": COLORS[shape_key],
            "x": GRID_WIDTH // 2 - 2,
            "y": 0,
        }

    def draw_grid(self):
        self.canvas.delete("all")
        for y, row in enumerate(self.grid):
            for x, cell_color in enumerate(row):
                if cell_color:
                    self.draw_cell(x, y, cell_color)
        self.draw_piece()

    def draw_cell(self, x, y, color):
        x1 = x * CELL_SIZE
        y1 = y * CELL_SIZE
        self.canvas.create_rectangle(
            x1, y1, x1 + CELL_SIZE, y1 + CELL_SIZE, fill=color, outline="gray"
        )

    def draw_piece(self):
        piece = self.current_piece
        for y, row in enumerate(piece["shape"]):
            for x, cell in enumerate(row):
                if cell == "#":
                    self.draw_cell(piece["x"] + x, piece["y"] + y, piece["color"])

    def move(self, dx, dy):
        if self.game_over:
            return
        self.current_piece["x"] += dx
        self.current_piece["y"] += dy
        if self.check_collision():
            self.current_piece["x"] -= dx
            self.current_piece["y"] -= dy
            if dy > 0:  # Jika nabrak ke bawah
                self.lock_piece()

    def rotate(self):
        if self.game_over:
            return
        piece = self.current_piece
        rotated_shape = ["".join(row) for row in zip(*piece["shape"][::-1])]
        original_shape = piece["shape"]
        piece["shape"] = rotated_shape
        if self.check_collision():
            piece["shape"] = original_shape  # Kembalikan jika nabrak

    def check_collision(self):
        piece = self.current_piece
        for y, row in enumerate(piece["shape"]):
            for x, cell in enumerate(row):
                if cell == "#":
                    new_x, new_y = piece["x"] + x, piece["y"] + y
                    if not (0 <= new_x < GRID_WIDTH and new_y < GRID_HEIGHT):
                        return True
                    if new_y >= 0 and self.grid[new_y][new_x]:
                        return True
        return False

    def lock_piece(self):
        piece = self.current_piece
        for y, row in enumerate(piece["shape"]):
            for x, cell in enumerate(row):
                if cell == "#":
                    grid_y, grid_x = piece["y"] + y, piece["x"] + x
                    if grid_y < 0:  # Game Over
                        self.game_over = True
                        self.canvas.create_text(
                            GRID_WIDTH * CELL_SIZE / 2,
                            GRID_HEIGHT * CELL_SIZE / 2,
                            text="GAME OVER",
                            font=("Arial", 30, "bold"),
                            fill="red",
                        )
                        return
                    self.grid[grid_y][grid_x] = piece["color"]

        self.clear_lines()
        self.current_piece = self.get_new_piece()
        if self.check_collision():
            self.game_over = True
            self.canvas.create_text(
                GRID_WIDTH * CELL_SIZE / 2,
                GRID_HEIGHT * CELL_SIZE / 2,
                text="GAME OVER",
                font=("Arial", 30, "bold"),
                fill="red",
            )

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.grid) if all(row)]
        if lines_to_clear:
            for i in lines_to_clear:
                del self.grid[i]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
            self.score += len(lines_to_clear) * 100
            self.score_label.config(text=f"Score: {self.score}")

    def game_loop(self):
        if not self.game_over:
            self.move(0, 1)
            self.draw_grid()
        self.after(GAME_SPEED, self.game_loop)


if __name__ == "__main__":
    app = TetrisApp()
    app.mainloop()
