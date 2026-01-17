import time

class GameManager:
    def __init__(self, question_count=20):
        self.question_count = question_count
        self.history_player1 = None  # history for the player 1 (thinks of object)
        self.history_player2 = None  # history for the player 2 (asks questions)

    def initialize_history(self, player1, player2, secret_object):
        # players only need context in case they are AI (to generate answers)
        # if both players AIs, they get their seperate contexts
        if player1.player_type == "ai":
            # set the context to answer questions regarding the secret object Player 1 (AI) created
            self.history_player1 = [{
                "role": "system",
                "content": f"""You are Player 1 in Twenty Questions. Your secret object is: '{secret_object}'.

                RULES:
                - ONLY answer 'yes', 'no', or 'maybe' if truly uncertain to yes/no questions
                - If the player asks a non yes/no question (like "what is it?" or "why?"), respond: "Please ask a yes/no question"
                - If the player guesses the EXACT object, respond: "Yes! It's {secret_object}. You win!"
                - If they guess something similar but not exact, respond: "Yes, but be more specific"
                - Stay in character - you are answering questions about your secret object, nothing else"""
            }]

        if player2.player_type == "ai":
            # set the context for the Player 2 (AI) to ask questions yes/no questions regarding the secret object
            self.history_player2 = [{
                "role": "system",
                "content": """You are Player 2 in Twenty Questions. Ask a CONCISE yes/no questions to guess the object.

                STRATEGY:
                - Questions 1-8: Start broad (alive? man-made? size? category?)
                - Questions 9-15: Narrow down specific features
                - Questions 16-20: Start making direct guesses - "Is it a [specific object]?"
                - Try different categories if previous guesses fail

                RULES:
                - Keep questions short
                - ONE question at a time
                - Output ONLY the question itself, no numbering or labels
                - After gathering enough information, make a direct guess. Keep in mind you have 20 questions until the game finishes"""
                    },
                    {
                        "role": "user",
                        "content": "I'm thinking of an object. You have 20 questions. Start!"
            }] 

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
        return player1.player_type == "ai" and player2.player_type == "ai"

    def play_game(self, player1, player2):
        """Main game loop where player 1 asks questions to player 2
        
        Args:
            player1: Player who thinks of an object
            player2: Player who asks questions
        """
        # player 1 thinks of an object
        secret_object = player1.think_of_an_object()
        questions_left = self.question_count
        
        # initalize histories based on player configurations
        self.initialize_history(player1, player2, secret_object)

        while questions_left > 0:
            current_question = self.question_count - questions_left + 1

            # player 2 asks a question
            question = player2.ask_question(self.history_player2, current_question) 
            self.update_history_with_question(question)
                
            # check for correct guess
            if self.verify_answer(question, secret_object):
                print("Player 2 guessed correctly!")
                print(f"The secret object was: {secret_object}")
                print(f"Questions used: {current_question}/20")
                return "player2"

            # add delay for AI vs AI mode (they are too quick sometimes)
            if self.is_ai_vs_ai(player1, player2):
                time.sleep(1)

            # player 1 answers the question
            answer = player1.answer_question(self.history_player1)
            self.update_history_with_answer(answer)
            
            # Add delay before next question in AI vs AI mode
            if self.is_ai_vs_ai(player1, player2):
                time.sleep(1)

            questions_left -= 1

        # If no questions left, then player 1 wins
        print("Player 1 wins!")
        print("Player 2 ran out of questions...")
        print(f"The secret object was: {secret_object}")
        return "player1"