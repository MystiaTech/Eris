from rule_engine import RuleEngine, Rule


class ContinuousLearning:
    def __init__(self, db_name):
        # Initialize RuleEngine
        self.rule_engine = RuleEngine(db_name)

    def add_initial_rules(self, rules):
        # Add initial rules to the rule engine
        for rule in rules:
            # Create Rule object from input tuple
            rule_obj = Rule(rule[0], rule[1])
            self.rule_engine.add_rule(rule_obj)

    def handle_user_input(self, user_input):
        # Match user input against rules
        matched_rule = self.rule_engine.match_rule(user_input)

        if matched_rule:
            # Retrieve output pattern from matched rule
            response = matched_rule.output_pattern
        else:
            # No match found, generate default response
            response = "I'm sorry, I didn't understand that."

        return response

    def capture_user_feedback(self, user_input, user_feedback):
        # Update rule based on user feedback
        # This is the continuous learning part, where the rule engine
        # is updated with new data based on user feedback to improve
        # its responses
        matched_rule = self.rule_engine.match_rule(user_input)
        if matched_rule:
            # Update output pattern of matched rule
            matched_rule.output_pattern = user_feedback
            self.rule_engine.update_rule(
                user_input,
                matched_rule.output_pattern
            )

    # Other methods for dynamic rule system functionality can be added here

    def process_message(self, user_input, user_feedback=None):
        # Implement message processing logic here
        # For example, you can call handle_user_input() to handle
        # the user input and return the response generated from
        # the matched rule's output pattern.
        if user_feedback:
            self.capture_user_feedback(user_input, user_feedback)
        response = self.handle_user_input(user_input)
        return response
