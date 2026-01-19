from abc import ABC, abstractmethod
from api_utils import get_ai_response, format_output_response
from game_config import GAME_OBJECTS
import random

class Player(ABC):
    """Abstract base class for all players, defining the interface for both human and AI players"""

    def __init__(self, player_type):
        self.player_type = player_type
        
    @abstractmethod
    def think_of_an_object(self):
        """Player 1 functionality: choose secret object"""
        pass

    @abstractmethod
    def ask_question(self, history, question_number):
        """Player 2 functionality: ask a yes/no question about the secret object"""
        pass

    @abstractmethod
    def answer_question(self, history):
        """Player 1 functionality: answer yes/no to the question posed by Player 2"""
        pass


class HumanPlayer(Player):
    """Human-controlled player that receives input from the command line interface"""

    def __init__(self, player_type="human"):
        super().__init__(player_type)

    def think_of_an_object(self):
        """Prompt human player to input a secret object for Player 2 to guess"""

        print("=== You are Player 1 ===")
        while True:
            secret_object = input("Please enter the object you would like for the Player 2 to guess: ").strip()
            if secret_object:  # checks if string is non-empty
                print(f"Secret object set: {secret_object}")
                print("The AI (Player 2) will now try to guess it!")
                return secret_object
            print("Object cannot be empty. Please try again.")

    def ask_question(self, history, question_number):
        """Prompt human player to input a yes/no question as Player 2"""

        while True:
            question = input(f"\nQuestion ({question_number}/20): ").strip()
            if question:
                return question
            print("Question cannot be empty. Please try again.")

    def answer_question(self, history):
        """Prompt human player to answer yes/no to a question about their secret object"""

        while True:
            answer = input("Your answer (yes/no): ").strip().lower()
            if answer in ['yes', 'no']:
                return answer
            print("Please answer 'yes' or 'no'")
    

class AIPlayer(Player):
    """AI-controlled player using LLM for decision making in both Player 1 and Player 2 roles"""

    def __init__(self, player_type="ai"):
        super().__init__(player_type)

    def think_of_an_object(self):
        """AI selects a secret object for Player 2 to guess using the object list"""

        print("The game has started! Please start asking questions.")

        secret_object = random.choice(GAME_OBJECTS)
        return secret_object


    def ask_question(self, history, question_number):
        """AI asks a strategic question as Player 2"""

        try:
            response = get_ai_response(history)
            question = format_output_response(response).strip()
            print(f"\nAI's Question ({question_number}/20): {question}")
            return question
        
        except Exception as e:
            print(f"There was an error getting AI question: {e}")
            raise 

    def answer_question(self, history):
        """AI generates a yes/no answer to a question about its secret object using conversation history"""

        try:
            response = get_ai_response(history)
            answer = format_output_response(response).strip()
            print(f"AI's answer: {answer}")
            return answer
        
        except Exception as e:
            print(f"There was an error getting AI response: {e}")
            raise