# Twenty Questions Game

A Python implementation of the Twenty Questions game, allowing human vs AI, AI vs human, and AI vs AI gameplay modes.

## Overview

This project implements the two-player game "Twenty Questions" where:
- **Player 1** thinks of a secret object
- **Player 2** asks up to 20 yes/no questions to guess the object
- Player 2 wins by correctly guessing the secret object within 20 questions

The implementation supports three gameplay modes:
1. Human as Player 1, AI as Player 2
2. AI as Player 1, Human as Player 2  
3. AI vs AI

## Project Structure

```
twenty-questions/
├── main.py              # Entry point and game mode selection
├── game.py              # GameManager class handling game flow
├── players.py           # Player classes (HumanPlayer, AIPlayer)
├── api_utils.py         # API utilities
├── prompts.py           # System prompts for AI players
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
├── .env                 # API credentials (not in repo)
├── .gitignore           # Git ignore configuration
└── README.md            # This file
```

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/vovij/Twenty-Questions-Game
cd Twenty-Questions-Game
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Create `.env` file**
```bash
cp .env.example .env
```

4. **Add your credentials to `.env`**
```env
LLM_API_KEY=your_api_key_here
BASE_URL=your_api_link_here
```

## Usage

Run the game:
```bash
python main.py
```

Choose a game mode:
- **Mode 1**: Human thinks of object, AI asks questions
- **Mode 2**: AI thinks of object, Human asks questions
- **Mode 3**: AI vs AI

Enjoy the game! 
Enter answers or questions when prompted to do so, or just watch 2 AI players play against each other.