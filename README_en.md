# Truco Paulista

![Truco Paulista Banner](images/background-img.jpg)

**Truco Paulista** is a digital implementation of the traditional Brazilian card game _Truco Paulista_. Developed in Python using the Pygame library, this game offers an engaging and interactive experience, allowing players to challenge an AI opponent with intuitive drag-and-drop mechanics and strategic gameplay.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Resources](#resources)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features

- **Interactive Gameplay:** Seamlessly drag and drop your cards onto the play area.
- **AI Opponent:** Play against an intelligent AI that automatically makes moves.
- **Truco Levels:** Progress through multiple levels of _Truco_—Truco, Seis, Nove, and Doze.
- **Dynamic Scoring:** Score points based on the outcome of each round and manage your total score to win the game.
- **Audio Integration:** Enjoy background music and sound effects for an immersive experience.
- **Modular Codebase:** Well-structured code divided into modules for easy maintenance and scalability.

## Installation

### Prerequisites

- **Python 3.6 or higher:** Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### Clone the Repository

```bash
git clone https://github.com/yuri-moraes/truco_paulista.git
cd truco_paulista
```

### Create a Virtual Environment (Optional but Recommended)

Creating a virtual environment helps manage dependencies and keep your project isolated.

```bash
python -m venv venv
```

Activate the virtual environment:

- **Windows:**

`bash
  venv\Scripts\activate
  `

- **macOS and Linux:**

`bash
  source venv/bin/activate
  `

### Install Dependencies

Ensure you have `pip` installed, then run:

```bash
pip install -r requirements.txt
```

**Note:** If there is no `requirements.txt` file, you can install the dependencies manually:

```bash
pip install pygame
```

## Usage

After completing the installation steps, you can start the game by running the main script.

```bash
python main.py
```

### Gameplay Instructions

1. **Starting the Game:**

- Upon launching, the game will display your hand of cards and the AI opponent's hidden cards.

2. **Playing a Card:**

- **Drag and Drop:** Click and hold a card from your hand, drag it to the play area on the table, and release to play.

3. **Truco Mechanics:**

- **Pedir Truco:** Click the "Pedir Truco" button to escalate the game stakes. The AI will automatically accept subsequent Truco levels—Seis, Nove, and Doze.
   - **Scoring:** Points are awarded based on the outcome of each round. The first player to reach or exceed 12 points wins the game.

4. **Game Over:**

- When a player reaches 12 points, the game declares the winner, plays the corresponding victory music, and automatically restarts for a new game.

## Project Structure

```
truco_paulista/
├── main.py
├── constants.py
├── resources.py
├── game_logic.py
├── utils.py
├── README.md
├── requirements.txt
├── images/
│   ├── background-img.jpg
│   ├── blank_card.png
│   ├── card1.png
│   ├── card2.png
│   └── ... (other card images)
└── sounds/
    ├── background-music.wav
    ├── winner-song.wav
    ├── looser-song.wav
    └── ... (other music and sound effects)
```

### File Descriptions

- **`main.py`**: The main file that initializes the game, manages the main loop, and coordinates interactions between modules.
- **`constants.py`**: Defines all constants used in the game, such as colors, screen sizes, directories, card orders, etc.
- **`resources.py`**: Responsible for loading game images and sounds.
- **`game_logic.py`**: Contains functions related to game logic, such as deck creation, manilha determination, card value, and game reset.
- **`utils.py`**: Utility functions, such as drawing text on the screen.
- **`images/`**: Folder containing all images used in the game.
- **`sounds/`**: Folder containing all audio files used in the game.
- **`README.md`**: This file.
- **`requirements.txt`**: List of Python dependencies required to run the game.

## Dependencies

The project uses the following libraries and frameworks:

- **[Pygame](https://www.pygame.org/news)**: Python library for game development. Used for graphics, sounds, and event management.

### Installing Dependencies

Dependencies are listed in the `requirements.txt` file. To install all dependencies, run:

```bash
pip install -r requirements.txt
```

**Contents of `requirements.txt`:**

```
pygame>=2.0.0
```

## Resources

### Images

All card images and the game background are located in the `images/` folder. Ensure that image files are correctly named and in `.png` or `.jpg` format.

- **`background-img.jpg`**: Game background image.
- **`blank_card.png`**: Image of the opponent's face-down card.
- **`cardX.png`**: Images of the deck's cards.

### Sounds

All audio files are located in the `sounds/` folder. Ensure that sound files are in `.wav` or `.mp3` format.

- **`background-music.wav`**: Background music that plays during the game.
- **`winner-song.wav`**: Music played when the player wins.
- **`looser-song.wav`**: Music played when the player loses.
- **Other sound effects**: Can be added as needed.

## Contributing

Contributions are welcome! If you wish to improve this project, follow the steps below:

1. **Fork the Repository**
2. **Create a Branch for your Feature (`git checkout -b feature/new-feature`)**
3. **Commit your Changes (`git commit -m 'Add new feature')`**
4. **Push to the Branch (`git push origin feature/new-feature`)**
5. **Open a Pull Request**

Please ensure to follow best coding practices and maintain consistency with the existing codebase.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- [Pygame](https://www.pygame.org/) - Library used for game development.
- [Freesound](https://freesound.org/) - Source of sound resources used in the game.
- [GitHub](https://github.com/) - Platform for hosting the source code.

---

**Developed with ❤️ by [Yuri Moraes](https://github.com/yuri-moraes)**
