import requests
import os
import json 
from api_utils import get_ai_response, format_output_response

class GameManager:
    def __init__(self, question_count, history):
        self.question_count = question_count
        self.history = history


    def choose_game_mode(self):
        """Let user choose which player they want to be"""
        print("=== Twenty Questions Game ===")
        print("1. Play as Player 1 (You think of object, AI asks questions)")
        print("2. Play as Player 2 (You ask questions, AI thinks of object)")
        
        while True:
            choice = input("Choose mode (1/2): ").strip()
            if choice in ["1", "2"]:
                return choice
            print("Invalid choice. Please enter 1 or 2")


    def get_secret_object_from_user(self):
        print("=== Twenty Questions Game ===")
        print("You are Player 1. Think of an object.")
        secret_object = input("Please enter the object you would like for the Player 2 to guess: ")
        print(f"Secret object set: {secret_object}")
        print("The AI (Player 2) will now try to guess it!")

        return secret_object


    def verify_answer(self, answer, secret_object):
        return secret_object.lower() in answer.strip().lower()


    def get_secret_object_from_ai(self):
        # Create a separate context for object selection
        object_selection_context = [{
            "role": "system",
            "content": """You are playing Twenty Questions. Think of a specific, concrete object for the other player to guess. 
            Respond with ONLY the object name, nothing else. Examples: 'bicycle', 'watch', 'piano'. Make it interesting but guessable."""
        },
        {
            "role": "user",
            "content": "Think of an object for me to guess in Twenty Questions. Respond with only the object name."
        }]
        try:
            response = get_ai_response(object_selection_context)
            secret_object = format_output_response(response).strip()

            # basic validation for the ai output (it outputs something reasonable)
            if not secret_object or len(secret_object) > 50:
                print("AI generated invalid object, using fallback: 'piano'")
                return "piano"

            print("AI thinks of a secret object...")
            return secret_object
        
        except Exception as e:
            print(f"Error getting object from AI: {e}")
            print("Using fallback object: 'piano'")
            return "piano"


    def game_mode1(self): # player 1 (user) thinks of an object, AI tries to guess it
        # give context to the model so it can play accordingly
        secret_object = self.get_secret_object_from_user()
        question_count = 20
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

        while question_count > 0:
            # get AI response
            try:
                ai_response = get_ai_response(self.history)
                ai_text = format_output_response(ai_response)
                print(f"Question number {21-question_count}/20: {ai_text}")
                self.history.append({"role": "assistant", "content": ai_text})

                # check if the AI guessed correctly
                if self.verify_answer(ai_text, secret_object):
                    print(f"AI has guessed the secret object {secret_object}! Game over...")
                    break

                # user answer to the AI's question
                user_answer = input("Your answer (yes/no): ").strip()
                self.history.append({"role": "user", "content": user_answer})

                question_count -= 1

            except Exception as e:
                print(f"There has been an error getting AI response: {e}")
                break
        
        # end of game message
        if question_count == 0:
            print(f"Congratulations, you won! AI ran out of questions...")


    def game_mode2(self): # user is a player 2 (asks questions), AI thinks of object
        secret_object = self.get_secret_object_from_ai()
        question_count = 20
        self.history = [{
            "role": "system",
            "content": f"""You are Player 1 in Twenty Questions. Your secret object is: '{secret_object}'.
            Here are the rules:
            1. ONLY answer 'yes', 'no', or 'maybe' if truly uncertain to yes/no questions
            2. If the player asks a non yes/no question (like "what is it?" or "why?"), respond: "Please ask a yes/no question"
            3. If the player guesses the EXACT object, respond: "Yes! It's {secret_object}. You win!"
            4. If they guess something similar but not exact, respond: "Yes, but be more specific"
            5. Stay in character - you are answering questions about your secret object, nothing else"""
        }]

        while question_count > 0:
            user_input = input(f"Question ({21-question_count}/20): ").strip()
            self.history.append({"role": "user", "content": user_input})
            # get AI response
            try:
                ai_response = get_ai_response(self.history)
                ai_text = format_output_response(ai_response)
                print("AI's response: ", ai_text)
                self.history.append({"role": "assistant", "content": ai_text})

            except Exception as e:
                print(f"There has been an error getting AI response: {e}")
                break

            question_count -= 1

            # check if the guess was correct
            if self.verify_answer(user_input, secret_object):
                print(f"Your guess is correct! You guessed the object: {secret_object}")
                print(f"Questions used: {20 - question_count}")
                break

        # end of game message
        if question_count == 0:
            print(f"Game Over! You ran out of questions...")
            print(f"The secret object was: {secret_object}")