# ♠️ AI Card Duel

**A single-player card duel against an AI opponent, built with Python and Pygame.**

Face off against an AI driven by four classic decision-making algorithms: **Breadth-First Search (BFS), Depth-First Search (DFS), Minimax and Expectimax**. The project shows how different search strategies change the behaviour of an opponent in a competitive game.

---

## 🎮 How to Play

1. Each side is dealt **5 cards** from a shuffled standard 52-card deck.
2. Every round, you pick a card; the AI picks one based on the chosen difficulty.
3. Both cards are revealed and compared. The higher card wins the round and scores **1 point**.
4. After **5 rounds**, the player with the most points wins.

### Card Values

| Card | Value |
|---|---:|
| 2–10 | Face value |
| Jack (J) | 11 |
| Queen (Q) | 12 |
| King (K) | 13 |
| Ace (A) | 14 |

---

## ✨ Features

- Standard 52-card deck with shuffling and dealing
- AI opponent powered by four algorithms
- Three difficulty levels: Easy, Medium and Hard
- Mouse-driven Pygame interface
- Live score and round tracking
- Automatic winner determination

---

## 🧠 AI Algorithms

| Difficulty | Algorithm | Approach |
|---|---|---|
| Easy | BFS | Scans the hand level by level using a queue |
| Medium | DFS | Recursively traverses the hand |
| Hard | Minimax / Expectimax | Adversarial and expected-value evaluation |

**Breadth-First Search (BFS)**
Uses a queue to visit cards level by level, tracking the highest-value card and returning it.

**Depth-First Search (DFS)**
Traverses the hand recursively, updating the best card found along the way.

**Minimax**
Models a maximising player against a minimising opponent and evaluates outcomes to choose a move.
*Current implementation uses recursive evaluation rather than a full game-tree search.*

**Expectimax**
Handles uncertainty by choosing the move with the best expected utility, averaging over the opponent's possible cards.
*Current implementation averages the remaining opponent card values rather than using explicit chance nodes.*

> **Why these four?** Together they contrast systematic search (BFS, DFS), adversarial reasoning (Minimax) and probabilistic decision-making (Expectimax).

---

## 🏗️ Architecture

The game is organised into six modules:

| Component | Responsibility |
|---|---|
| Deck Management | Creates, shuffles and deals cards |
| Player Interface | Handles mouse-based card selection |
| AI Decision Module | Picks a card according to difficulty |
| Round Resolution | Compares cards and updates scores |
| Game Controller | Manages game states, turns and rounds |
| GUI | Renders cards, scores, rounds, buttons and results |

### Game Flow

```text
        START GAME
             |
             v
     Create 52-Card Deck
             |
             v
       Shuffle & Deal
             |
             v
    Player and AI Select Cards
             |
             v
      Reveal Both Cards
             |
             v
      Compare Card Values
             |
             v
        Update Scores
             |
             v
        Next Round?
         /       \
       Yes        No
        |          |
        v          v
     Repeat    Final Result
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3 | Core language and game logic |
| Pygame | Graphics and event handling |
| `random` | Deck shuffling |
| `collections.deque` | Queue for BFS |
| `math`, `sys` | Calculations and clean program exit |
| Object-Oriented Programming | Structuring game components as classes |

**Developed with:** PyCharm and Visual Studio Code

---

## 🚀 Getting Started

**Prerequisites:** Python 3.x and pip

```bash
# 1. Clone the repository
git clone https://github.com/harshal-sal/AI-duel-Card-Game.git

# 2. Move into the project folder
cd AI-duel-Card-Game

# 3. Install dependencies
pip install pygame

# 4. Run the game
python "AI DUEL CARD Game.py"
```

---

## 🔮 Roadmap

- [ ] Full game-tree search for Minimax
- [ ] Explicit chance nodes for Expectimax
- [ ] Additional difficulty levels
- [ ] Gameplay statistics and algorithm performance comparison
- [ ] Sound effects and animations
- [ ] Improved GUI

---

## 🎓 About the Project

| | |
|---|---|
| **Project** | AI Card Duel |
| **Category** | Artificial Intelligence Mini Project |
| **Department** | Computer Engineering |
| **Institution** | Padre Conceicao College of Engineering |

## 👨‍💻 Author

**Harshal Prakash Salunke** · [@harshal-sal](https://github.com/harshal-sal)

---

⭐ If you enjoyed this project, consider giving the repository a star!

*Built with Python, Artificial Intelligence and a competitive spirit. ♠️*
