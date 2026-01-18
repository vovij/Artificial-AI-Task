from game import GameManager
from players import AIPlayer

# quick way to test AI vs AI multiple times
for i in range(5):
    print(f"\n=== Game {i+1} ===")
    game = GameManager()
    game.play_game(AIPlayer(), AIPlayer())