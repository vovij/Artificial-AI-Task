from abc import ABC, abstractmethod
from api_utils import get_ai_response, format_output_response
from prompts import OBJECT_SELECTION_SYSTEM_PROMPT

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
        secret_object = input("Please enter the object you would like for the Player 2 to guess: ").strip()
        print(f"Secret object set: {secret_object}")
        print("The AI (Player 2) will now try to guess it!")
        return secret_object

    def ask_question(self, history, question_number):
        """Prompt human player to input a yes/no question as Player 2"""

        question = input(f"\nQuestion ({question_number}/20): ").strip()
        return question

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
        """AI selects a secret object for Player 2 to guess using LLM"""

        # Use a separate context for AI object selection
        object_selection_context = [{"role": "system", "content": OBJECT_SELECTION_SYSTEM_PROMPT}]
        try:
            print("AI thinks of a secret object...")
            response = get_ai_response(object_selection_context)
            secret_object = format_output_response(response).strip()

            # basic validation for the AI output (it outputs something reasonable)
            if not secret_object or len(secret_object) > 50:
                raise ValueError("AI generated invalid object")
            return secret_object
        
        except Exception as e:
            print(f"There was an error getting object from AI: {e}")
    
    def ask_question(self, history, question_number):
        """AI asks a strategic question as Player 2"""

        try:
            response = get_ai_response(history)
            question = format_output_response(response).strip()
            print(f"\nAI Question ({question_number}/20): {question}")
            return question
        
        except Exception as e:
            print(f"There was an error getting AI question: {e}")

    def answer_question(self, history):
        """AI generates a yes/no answer to a question about its secret object using conversation history"""

        try:
            response = get_ai_response(history)
            answer = format_output_response(response).strip()
            print(f"AI's answer: {answer}")
            return answer
        
        except Exception as e:
            print(f"There was an error getting AI response: {e}")