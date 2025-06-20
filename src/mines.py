"""Kalimotxo's Minesweeper Game.

A simple implementation of Minesweeper using Tkinter and NumPy.
"""

import tkinter as tk
from functools import partial
from itertools import product
from typing import List, Tuple

import numpy as np
from PIL import Image, ImageTk

# Global button list
button_ids: List[tk.Button] = []


def get_random_coords(xmax: int, ymax: int) -> Tuple[int, int]:
    """Generate random (x, y) coordinates within field bounds."""
    x = np.random.randint(0, xmax)
    y = np.random.randint(0, ymax)
    return x, y


def count_adjacent_mines(
    x: int, y: int, xmax: int, ymax: int, field: np.ndarray
) -> int:
    """Count how many mines surround the cell at (x, y)."""
    offsets = product([-1, 0, 1], repeat=2)
    count = 0
    for dx, dy in offsets:
        if dx == dy == 0:
            continue
        nx, ny = x + dx, y + dy
        if 0 <= nx < xmax and 0 <= ny < ymax and field[nx, ny] == np.inf:
            count += 1
    return count


def generate_minefield(xsize: int, ysize: int, mines: int) -> np.ndarray:
    """Create the game field with the given size and number of mines."""
    field = np.zeros((xsize, ysize))
    placed = 0
    while placed < mines:
        x, y = get_random_coords(xsize, ysize)
        if field[x, y] != np.inf:
            field[x, y] = np.inf
            placed += 1
    for x in range(xsize):
        for y in range(ysize):
            if field[x, y] != np.inf:
                field[x, y] = count_adjacent_mines(x, y, xsize, ysize, field)
    return field


def reveal_cell(index: int, minefield: np.ndarray) -> None:
    """Reveals a cell and ends the game if it's a mine."""
    button = button_ids[index]
    row = button.grid_info()["row"]
    col = button.grid_info()["column"]
    value = minefield[row, col]

    if value == np.inf:
        button.configure(bg="black", text="💣")
        game_over()
        return

    colors = {
        0: "white",
        1: "pale green",
        2: "yellow green",
        3: "yellow",
        4: "orange",
        5: "dark orange",
        6: "orange red",
        7: "red2",
        8: "red3",
    }
    button.configure(
        text=str(int(value)), bg=colors.get(int(value), "white"), state="disabled"
    )


def game_over() -> None:
    """Display game over popup and reset game on close."""
    new_window = tk.Toplevel()
    new_window.title("GAME OVER")
    frame = tk.Frame(new_window)
    frame.pack(padx=20, pady=20)
    tk.Label(frame, text="BUUUM!!\n\nYou hit a mine!").pack()

    def close_and_reset():
        # Destroy game window(s)
        for widget in tk._default_root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()
        # Clear buttons
        button_ids.clear()
        new_window.destroy()

    tk.Button(frame, text="Close", command=close_and_reset).pack(pady=10)


def create_game_window(rows: int, cols: int, minefield: np.ndarray) -> None:
    """Create the minefield game window."""
    game_window = tk.Toplevel()
    game_window.title("Kalimotxo's Minesweeper")
    frame = tk.Frame(game_window)
    frame.grid(row=0, column=0)

    positions = list(product(range(rows), range(cols)))
    for idx, (r, c) in enumerate(positions):
        button = tk.Button(
            frame,
            text="?",
            width=3,
            height=1,
            command=partial(reveal_cell, index=idx, minefield=minefield),
        )
        button.grid(row=r, column=c, sticky="nsew")
        button_ids.append(button)

    tk.Button(game_window, text="Close", command=game_window.destroy).grid(
        row=rows + 1, column=0, pady=10
    )


def on_start_game(
    entry_rows: tk.Entry, entry_cols: tk.Entry, entry_mines: tk.Entry
) -> None:
    """Triggered when the start button is clicked; reads input and starts game."""
    try:
        rows = int(entry_rows.get())
        cols = int(entry_cols.get())
        mines = int(entry_mines.get())
        if mines >= rows * cols:
            raise ValueError("Too many mines.")
        minefield = generate_minefield(rows, cols, mines)
        create_game_window(rows, cols, minefield)
    except ValueError as e:
        tk.messagebox.showerror("Invalid input", str(e))


def main() -> None:
    """Run the Minesweeper launcher GUI."""
    root = tk.Tk()
    root.title("Kalimotxo's Minesweeper")
    root.geometry("700x400")

    # Layout
    left = tk.Frame(root, borderwidth=2, relief="solid")
    right = tk.Frame(root, borderwidth=2, relief="solid")
    left.pack(side="left", expand=True, fill="both")
    right.pack(side="right", expand=True, fill="both")

    # Left (image box)
    box1 = tk.Frame(left)
    box1.pack(expand=True, fill="both", padx=5, pady=5)
    tk.Label(box1, text=" ").pack()
    img = Image.open("assets/mine.png")
    photo = ImageTk.PhotoImage(img)
    box1.image = photo  # Prevent garbage collection
    tk.Label(box1, image=photo).pack()

    # Right (control panel)
    box2 = tk.Frame(right)
    box2.pack(expand=True, fill="both", padx=5, pady=5)
    tk.Label(box2, text="\nEnter the field characteristics\n").pack()

    tk.Label(box2, text="Number of rows").pack()
    entry_rows = tk.Entry(box2)
    entry_rows.pack()

    tk.Label(box2, text="Number of columns").pack()
    entry_cols = tk.Entry(box2)
    entry_cols.pack()

    tk.Label(box2, text="Number of mines").pack()
    entry_mines = tk.Entry(box2)
    entry_mines.pack()

    tk.Button(
        box2,
        text="Start Game",
        command=lambda: on_start_game(entry_rows, entry_cols, entry_mines),
    ).pack(pady=10)

    tk.Button(box2, text="Exit", command=root.destroy).pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()
