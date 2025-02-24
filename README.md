# Falcon Hunter - 2D OpenGL Game

**Falcon Hunter** is an interactive 2D game built with Python using OpenGL/GLUT. Control a hunter to shoot falcons, avoid obstacles, and survive in a dynamic day/night cycling world.

---

## Features

- 🎯 Shoot falcons with 'B' key
- 🦘 Procedural leg animation & jumping physics
- 🌗 Smooth day/night transitions
- 🚧 Randomly generated obstacles
- 🎮 Pause/resume functionality
- 🕹️ Game Over on 3 collisions or 5 missed falcons

---

## Technologies

- Python 3
- OpenGL/GLUT
- Midpoint Circle Algorithm
- Bresenham's Line Algorithm
- Object-Oriented Programming

---

## How to Run

### Prerequisites

1. **Python 3**: Install from [python.org](https://www.python.org/).
2. **VS Code**: Install from [code.visualstudio.com](https://code.visualstudio.com/).

---

### Steps

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/falcon-hunter.git
   cd falcon-hunter
   ```
2. Install dependencies:
   ```bash
   pip install PyOpenGL PyOpenGL_accelerate
   ```
3. Run the game:
   ```bash
   python main.py
   ```

---

### VS Code Setup

1. Open the project folder in VS Code.
2. Open the terminal (`Ctrl + ``).
3. Run:
   ```bash
   pip install PyOpenGL PyOpenGL_accelerate
   python main.py
   ```

---

### Troubleshooting

- **Missing GLUT**:
  - Ubuntu/Debian: `sudo apt-get install freeglut3-dev`
  - Windows: Ensure OpenGL is installed.
  - macOS: Pre-installed.
- **Virtual Environment (Optional)**:
  ```bash
  python -m venv venv
  source venv/bin/activate  # Windows: venv\Scripts\activate
  pip install PyOpenGL PyOpenGL_accelerate
  python main.py
  ```

---

## Gameplay

1. Enter hunter name at launch.
2. Controls:
   - **SPACE**: Jump
   - **B**: Shoot
   - **Left-click UI**: Reset/Pause/Exit
3. Objective: Maximize score by shooting falcons and avoiding obstacles.

---

## Code Highlights

- Custom midpoint circle algorithm
- State machine for game phases
- Linear interpolation for animations
- Event-driven input handling

---

## License

MIT License. Open-source and free to use.

Enjoy the game! 🎮

```

```
