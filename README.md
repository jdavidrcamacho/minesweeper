# 🧨 Minesweeper

A simple Python version of the classic Microsoft Minesweeper game, built with `tkinter`. This is a fun terminal-friendly GUI game for learning or nostalgic fun.

![Minesweeper Screenshot](assets/mine.png)

## 🚀 Features

- Interactive GUI built with `tkinter`
- Customizable grid size and number of mines
- Basic visual feedback for mine hits and number hints
- Clean and modular codebase with type hints and docstrings

## 🛠 Requirements

- Python 3.8+
- Managed with [Poetry](https://python-poetry.org/)

## ⚙️ Setup & Installation

Clone the repository, then install dependencies using Poetry:

```bash
poetry install
```

Activate the virtual environment:

```bash
poetry shell
```

▶️ How to Run

Inside the Poetry shell or your activated environment:

```
python src/mines.py
```

Or with IPython:

```
%run src/mines.py
```

    Note: The image file assets/mine.png must exist for the GUI to display correctly.

💡 Development & Checks

You can run formatting, linting, typing, and docstring checks using make (if you have a Makefile):

```
make static-check
```

To automatically fix formatting issues:

```
make format-fix
```

📦 Project Structure

```
minesweeper/
├── src/
│   └── mines.py          # Main game logic and GUI
├── assets/
│   └── mine.png          # Mine image used in GUI
├── pyproject.toml        # Poetry configuration and dependencies
├── Makefile              # Dev automation tasks
└── README.md             # You're reading it!
```

👨‍💻 Author

2019–2025 — João Camacho

Feel free to contribute, fork, or suggest improvements!


---
