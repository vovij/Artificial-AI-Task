class GameManager:
    def __init__(self, question_count=20):
        self.question_count = question_count
        self.history = []

    def initialize_history(self, player1, player2, secret_object):
        if player1.player_type == "human" and player2.player_type == "ai":
            self.history = [{
                "role": "system",
                "content": """You are Player 2 in Twenty Questions. Ask CONCISE yes/no questions to guess the object.

                STRATEGY:
                - Questions 1-8: Start broad (alive? man-made? size? category?)
                - Questions 9-15: Narrow down specific features
                - Questions 16-20: Start making direct guesses - "Is it a [specific object]?"

                RULES:
                - Keep questions short
                - ONE question at a time
                - After gathering enough information, make a direct guess. Keep in mind you have 20 questions until the game finishes"""
                    },
                    {
                        "role": "user",
                        "content": "I'm thinking of an object. You have 20 questions. Start!"
            }] 

        elif player1.player_type == "ai" and player2.player_type == "human":
            self.history = [{
                "role": "system",
                "content": f"""You are Player 1 in Twenty Questions. Your secret object is: '{secret_object}'.
                Here are the rules:
                - ONLY answer 'yes', 'no', or 'maybe' if truly uncertain to yes/no questions
                - If the player asks a non yes/no question (like "what is it?" or "why?"), respond: "Please ask a yes/no question"
                - If the player guesses the EXACT object, respond: "Yes! It's {secret_object}. You win!"
                - If they guess something similar but not exact, respond: "Yes, but be more specific"
                - Stay in character - you are answering questions about your secret object, nothing else"""
            }]

        elif player1.player_type == "ai" and player2.player_type == "ai":
            self.history = None # implement AI vs AI logic TODO
            pass

    def verify_answer(self, answer, secret_object):
        """Check if a guess matches the secret object"""
        return secret_object.lower() in answer.strip().lower()
    
    def play_game(self, player1, player2):
        """Main game loop where player 1 asks questions to player 2
        
        Args:
            player1: Player who thinks of an object
            player2: Player who asks questions
        """
        # player 1 thinks of an object
        secret_object = player1.think_of_an_object()
        questions_left = self.question_count
        
        # initalize conversation history
        self.initialize_history(player1, player2, secret_object)

        while questions_left > 0:
            current_question = self.question_count - questions_left + 1

            # player 2 asks a question
            question = player2.ask_question(self.history, current_question) 
            self.history.append({"role": "user", "content": question})

            if self.verify_answer(question, secret_object):
                print("Player 2 guessed correctly!")
                print(f"The secret object was: {secret_object}")
                print(f"Questions used: {current_question}/20")
                return "player2"

            # player 1 answers the question
            answer = player1.answer_question(self.history)

            # add answer to the history
            self.history.append({"role": "assistant", "content": answer})

            questions_left -= 1

        # If no questions left, then player 1 wins
        print("Player 1 wins!")
        print("Player 2 ran out of questions...")
        print(f"The secret object was: {secret_object}")
        return "player1"