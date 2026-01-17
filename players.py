from abc import ABC, abstractmethod
from api_utils import get_ai_response, format_output_response

class Player(ABC):
    """Abstract base class for all players"""
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
    def __init__(self, player_type="human"):
        super().__init__(player_type)

    def think_of_an_object(self):
        print("=== You are Player 1 ===")
        secret_object = input("Please enter the object you would like for the Player 2 to guess: ").strip()
        print(f"Secret object set: {secret_object}")
        print("The AI (Player 2) will now try to guess it!")
        return secret_object

    def ask_question(self, history, question_number):
        """Human asks a question as Player 2"""
        question = input(f"\nQuestion ({question_number}/20): ").strip()
        return question

    def answer_question(self, history):
        """Human answers AI's question"""
        answer = input("Your answer (yes/no): ").strip().lower()
        return answer
    

class AIPlayer(Player):
    def __init__(self, player_type="ai"):
        super().__init__(player_type)

    def think_of_an_object(self):
        # Create a separate context for AI object selection
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
            print("AI thinks of a secret object...")
            response = get_ai_response(object_selection_context)
            secret_object = format_output_response(response).strip()

            # basic validation for the ai output (it outputs something reasonable)
            if not secret_object or len(secret_object) > 50:
                print("AI generated invalid object, please try again.")
            return secret_object
        
        except Exception as e:
            print(f"Error getting object from AI: {e}")
    
    def ask_question(self, history, question_number):
        """AI asks a strategic question as Player 2"""
        try:
            response = get_ai_response(history)
            question = format_output_response(response).strip()
            print(f"\nAI Question ({question_number}/20): {question}")
            return question
        
        except Exception as e:
            print(f"Error getting AI question: {e}")

    def answer_question(self, history):
        """AI answers a question about its secret object"""
        try:
            response = get_ai_response(history)
            answer = format_output_response(response).strip()
            print(f"AI's answer: {answer}")
            return answer
        
        except Exception as e:
            print(f"Error getting AI response: {e}")