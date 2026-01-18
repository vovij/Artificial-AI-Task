from game import GameManager
from players import HumanPlayer, AIPlayer

def print_welcome_message():
    """Display beautiful welcome message for the game"""
    
    print("\n" + "=" * 57)
    print(" " * 15 + "◇  TWENTY QUESTIONS GAME  ◇")
    print("=" * 57)
    print()
    print("  Welcome to Twenty Questions Game!")
    print("  One player thinks of an object, the other asks yes/no questions.")
    print("  The goal of the game is to guess the secret object in 20 questions or less.")
    print()

def print_game_modes():
    """Display available game modes"""
    
    print()
    print(" " * 18 + "+" + "-" * 18 + "+")
    print(" " * 18 + "|{:^{w}}|".format("▶▶▶ GAME MODES ◀◀◀", w=18))
    print(" " * 18 + "+" + "-" * 18 + "+")
    print()    
    print()    
    print("  1. Play as Player 1 (You think of object, AI asks questions)")
    print("  2. Play as Player 2 (You ask questions, AI thinks of object)")
    print("  3. AI vs AI (Two AIs play against each other)")
    print()
    print("=" * 57)
    print()


if __name__ == "__main__":
    """Main initialization point"""

    # display welcome message
    print_welcome_message()
    
    # display game modes
    print_game_modes()

    while True: # user chooses game mode through CLI
        mode = input("Choose mode (1/2/3): ").strip()
        if mode in ["1", "2", "3"]:
            break 
        print("Please enter valid game mode (1, 2 or 3)")

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

