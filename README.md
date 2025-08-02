# Python Projects

This repository contains a collection of enhanced Python projects, ranging from beginner to advanced level. Each project has been improved for better user experience, code quality, and features.

---

## 🚀 Requirements
- Python 3.7 or higher
- Recommended: Virtual environment (venv)
- Some projects require additional packages (see below)
- Any code editor (VS Code, PyCharm, Sublime Text, etc.)

---

## 📦 Installation & Setup

### Step 1: Clone the Repository
```bash
git clone <repo-url>
cd Python-Projects
```

### Step 2: Create a Virtual Environment (Recommended)
**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
# Install all dependencies for all projects
pip install -r requirements.txt
```

**Or install dependencies individually:**
```bash
# For basic projects (no extra dependencies needed)
# - hangman.py, tictactoegame.py, numberguessgame.py, wordguess.py
# - mazesolver.py, slotmachine.py, rockpaperscissor.py

# For Snake Game
pip install pygame

# For Image Displayer GUI
pip install PyQt5

# For PDF Merger
pip install PyPDF2

# For Password Manager
pip install cryptography

# For RoboTalker (choose one or more)
pip install pyttsx3  # Cross-platform TTS
pip install gtts     # Google TTS

# For Weather App
pip install requests
```

### Step 4: Run Projects
```bash
# Example: Run Hangman
python hangman.py

# Example: Run Snake Game
python snakegame.py
```

---

## 🕹️ Project List & Features

### 1. Hangman (`hangman.py`)
- Classic word guessing game with multiple categories (fruits, animals, countries, colors)
- ASCII art, hints, statistics tracking, and improved UI
- No extra dependencies

### 2. Tic Tac Toe (`tictactoegame.py`)
- Play against the computer with 3 AI difficulty levels (Easy, Medium, Hard)
- Statistics tracking and improved interface
- No extra dependencies

### 3. Number Guess Game (`numberguessgame.py`)
- Guess a random number with difficulty levels, hints, and stats
- No extra dependencies

### 4. Word Guess (Lingo) (`wordguess.py`)
- Guess 4-letter words with no repeated letters
- Feedback for correct/wrong positions, stats, and replay
- Uses `doc/words.txt` (included)

### 5. Maze Solver (`mazesolver.py`)
- Visualizes and solves mazes using DFS, BFS, A*, and Dijkstra's algorithms
- Interactive CLI with algorithm comparison
- No extra dependencies

### 6. Slot Machine (`slotmachine.py`)
- Simulated slot machine with multiple paylines, bonus features, and progressive jackpot
- Enhanced graphics and statistics
- No extra dependencies

### 7. Rock Paper Scissors (`rockpaperscissor.py`)
- Play against an AI with 3 difficulty levels
- Tracks win/loss/tie stats and move history
- No extra dependencies

### 8. Snake Game (`snakegame.py`)
- Classic Snake with power-ups, levels, high score saving, and improved graphics
- Requires `pygame` (`pip install pygame`)

### 9. Image Displayer GUI (`imagedisplayerGUI.py`)
- Modern PyQt5 GUI to view, zoom, and apply filters to images
- Requires `PyQt5` (`pip install PyQt5`)

### 10. PDF Merger (`pdfmerger.py`)
- Merge multiple PDFs via a GUI or CLI
- Requires `PyPDF2` and `tkinter` (`pip install PyPDF2`)

### 11. Password Manager (`passwordmanager.py`)
- Secure password storage with encryption, password generation, search, and stats
- Requires `cryptography` (`pip install cryptography`)

### 12. RoboTalker (`robotalker.py`)
- Text-to-speech with multiple engine support (wsay, pyttsx3, gtts, festival)
- Requires `pyttsx3` and/or `gtts` for advanced features

### 13. Weather App (`weatherapp.py`)
- Fetches current weather for any city, supports multiple APIs and units
- Requires `requests` (`pip install requests`)

---

## 📝 Notes
- For best experience, install all dependencies listed above.
- Some projects (like Snake, Image Displayer, PDF Merger) require additional libraries.
- For `robotalker.py`, Windows users can use `wsay.exe` (see [wsay](https://github.com/p-groarke/wsay)), or use `pyttsx3`/`gtts` for cross-platform support.
- The `doc/words.txt` file is required for the Word Guess game.
- Virtual environment is recommended to avoid conflicts with system Python packages.

---

## 🤝 Contributing
Contributions are welcome! If you have a project or improvement, please create a pull request with a description and usage instructions.

---

## 📄 License
This repository is open source and available under the MIT License.
