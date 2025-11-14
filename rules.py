# rules.py

class Rules:
    def __init__(self, input_pattern, output_pattern):
        self.input_pattern = input_pattern
        self.output_pattern = output_pattern


# Original rules
original_rules = [
    Rules("hello", "Hi there!"),
    Rules("hi", "Hello!"),
    Rules("how are you", "I'm doing well, thank you!"),
    Rules("what's your name", "My name is Eris!"),
    Rules("goodbye", "Goodbye!"),
    Rules("bye", "See you later!"),
    # Add more original rules as needed
]

# User feedback-based rules
user_feedback_rules = [
    # Add rules based on user feedback here
]

# Autonomous rules
autonomous_rules = [
    # Add rules developed by the chatbot on its own free-will here
]

# Combine all sets of rules into a single list
all_rules = original_rules + user_feedback_rules + autonomous_rules
