# Falcon Hunter - 2D OpenGL Game

**Falcon Hunter** is an interactive 2D game built with Python using OpenGL/GLUT, featuring dynamic gameplay mechanics and real-time collision detection. Control a hunter character to shoot falcons, avoid obstacles, and survive environmental challenges in a day/night cycling world.

## Features
- 🎯 **Falcon Shooting Mechanics**: Fire bullets with 'B' key
- 🦘 **Procedural Animation**: Character leg movement & jumping physics
- 🌗 **Dynamic Environment**: Smooth day/night transitions with color interpolation
- 🚧 **Obstacle System**: Randomly generated barriers with collision detection
- 🎮 **Game State Management**: Pause/resume functionality and score tracking
- 🕹️ **Challenge System**: 
  - 3 collisions → Game Over
  - 5 missed falcons → Game Over

## Technologies
- Python 3
- OpenGL/GLUT graphics
- Midpoint Circle Algorithm (custom implementation)
- Bresenham's Line Algorithm (optimized)
- Object-Oriented Programming

## Installation
```bash
pip install pyopengl glut
git clone https://github.com/yourusername/falcon-hunter.git
cd falcon-hunter
python main.py```
