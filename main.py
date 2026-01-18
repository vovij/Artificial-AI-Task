from game import GameManager
from players import HumanPlayer, AIPlayer

if __name__ == "__main__":
    """Main initialization point"""

    print("=== Twenty Questions Game ===")
    print("1. Play as Player 1 (You think of object, AI asks questions)")
    print("2. Play as Player 2 (You ask questions, AI thinks of object)")
    print("3. AI vs AI (Two AIs play against each other)")

    while True: # user chooses game mode through CLI
        mode = input("Choose mode (1/2/3): ").strip()
        if mode in ["1", "2", "3"]:
            break 
        print("Please enter either valid game mode")

    # initialize the game using GameManager
    game = GameManager(question_count=20)

    if mode == "1":
        player1 = HumanPlayer()
        player2 = AIPlayer()

    elif mode == "2":
        player1 = AIPlayer()
        player2 = HumanPlayer()

    elif mode == "3":
        player1 = AIPlayer()
        player2 = AIPlayer()

    game.play_game(player1, player2)