from game import GameManager

if __name__ == "__main__":
    # initialize the game
    game = GameManager(question_count=20, history=[])
    mode = game.choose_game_mode() # choose game mode
    
    if mode == "1":
        game.game_mode1()
    elif mode == "2":
        game.game_mode2()