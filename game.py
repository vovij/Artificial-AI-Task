import time
from prompts import PLAYER1_SYSTEM_PROMPT, PLAYER2_SYSTEM_PROMPT

class GameManager:
    """Manages game state, flow, and conversation histories for Twenty Questions game between two players"""

    def __init__(self, question_count=20):
        self.question_count = question_count
        self.history_player1 = None  # history for Player 1 (thinks of object)
        self.history_player2 = None  # history for Player 2 (asks questions)

    def initialize_history(self, player1, player2, secret_object):
        """Initialize conversation histories with role-specific prompts for AI players"""

        # players only need context in case they are AI (to generate answers)
        # if both players are AIs, they get their seperate contexts
        if player1.player_type == "ai":
            # set the context to answer questions regarding the secret object Player 1 (AI) created
            self.history_player1 = [{"role": "system", "content": PLAYER1_SYSTEM_PROMPT.format(secret_object)}]

        if player2.player_type == "ai":
            # set the context for the Player 2 (AI) to ask questions yes/no questions regarding the secret object
            self.history_player2 = [{"role": "system", "content": PLAYER2_SYSTEM_PROMPT}]

    def verify_answer(self, answer, secret_object):
        """Check if a guess matches the secret object"""

        return secret_object.lower() in answer.strip().lower()
    
    def update_history_with_question(self, question):
        """Update histories after player2 asks a question"""

        if self.history_player1 is not None:
            self.history_player1.append({"role": "user", "content": question})
        if self.history_player2 is not None:
            self.history_player2.append({"role": "assistant", "content": question})

    def update_history_with_answer(self, answer):
        """Update histories after player1 answers a question"""

        if self.history_player1 is not None:
            self.history_player1.append({"role": "assistant", "content": answer})
        if self.history_player2 is not None:
            self.history_player2.append({"role": "user", "content": answer})

    def is_ai_vs_ai(self, player1, player2):
        """Check if both players are AI"""

        return player1.player_type == "ai" and player2.player_type == "ai"

    def play_game(self, player1, player2):
        """Main game loop where player2 asks questions to guess player1's object"""

        # player 1 thinks of an object
        secret_object = player1.think_of_an_object()
        current_question = 1 # keep track for current question
        
        # initalize histories based on player configurations
        self.initialize_history(player1, player2, secret_object)

        while current_question <= self.question_count:
            # player 2 asks a question
            question = player2.ask_question(self.history_player2, current_question) 
            self.update_history_with_question(question)

            # check if the guess of player 2 was correct
            if self.verify_answer(question, secret_object):
                print("Player 2 guessed correctly!")
                print(f"The secret object was: {secret_object}")
                print(f"Questions used: {current_question}/{self.question_count}")
                return "player2"

            # add delay for AI vs AI mode (responses are too quick sometimes)
            if self.is_ai_vs_ai(player1, player2):
                time.sleep(1)

            # player 1 answers the question
            answer = player1.answer_question(self.history_player1)
            self.update_history_with_answer(answer)

            # Add delay before next question in AI vs AI mode
            if self.is_ai_vs_ai(player1, player2):
                time.sleep(1)

            current_question += 1

        # If no questions left, then player 1 wins
        print("Player 1 wins!")
        print("Player 2 ran out of questions...")
        print(f"The secret object was: {secret_object}")
        return "player1"
    
        # returning player1 or player2 can be used further to evaluate performance for different AI prompts in future implementations