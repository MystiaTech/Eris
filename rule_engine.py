import sqlite3
import datetime


class Rule:
    def __init__(self, input_pattern, output_pattern):
        self.input_pattern = input_pattern
        self.output_pattern = output_pattern

    def match(self, user_input):
        # Implement matching logic here
        # For example, you can check if the user_input matches
        # the input_pattern using a regular expression or any other
        # suitable matching technique
        return self.input_pattern in user_input

    def update(self, user_input, user_feedback):
        """
        Update rule based on user feedback.

        Args:
            user_input: The input that matched this rule
            user_feedback: Rating from 1-5, or None if no feedback given

        Note:
            Currently stores feedback for potential future use.
            Could be extended to adjust output_pattern based on ratings.
        """
        # Store feedback for potential future enhancements
        # Low ratings (1-2) could trigger rule modification
        # High ratings (4-5) reinforce the rule
        if user_feedback is not None and user_feedback < 3:
            # Future enhancement: adjust or flag rule for review
            pass


class RuleDB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        # Create rules table if not exists
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS rules (
                input_pattern TEXT PRIMARY KEY,
                output_pattern TEXT,
                last_changed TEXT
            )
        ''')
        self.conn.commit()

    def add_rule(self, rule):
        # Add rule to the database
        # Handle exceptions if rule already exists
        try:
            self.cursor.execute(
                "INSERT INTO rules "
                "(input_pattern, output_pattern, last_changed) "
                "VALUES (?, ?, ?)",
                (rule.input_pattern, rule.output_pattern,
                 str(datetime.datetime.now()))
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("Rule already exists in the database.")

    def update_rule(self, rule):
        # Update the rule in the database
        self.cursor.execute(
            "UPDATE rules SET output_pattern = ?, last_changed = ? "
            "WHERE input_pattern = ?",
            (rule.output_pattern, str(datetime.datetime.now()),
             rule.input_pattern)
        )
        self.conn.commit()

    def get_rules(self):
        # Retrieve rules from the database
        self.cursor.execute("SELECT input_pattern, output_pattern FROM rules")
        rows = self.cursor.fetchall()
        rules = []
        for row in rows:
            input_pattern, output_pattern = row
            rule = Rule(input_pattern, output_pattern)
            rules.append(rule)
        return rules


class RuleEngine:
    def __init__(self, rule_db):
        self.rules = []
        self.rule_db = rule_db
        # Load rules from database
        self.load_rules_from_db()

    def add_rule(self, rule):
        # Add rule to the RuleDB
        self.rule_db.add_rule(rule)
        # Also add to in-memory rules list for immediate matching
        # Check if rule already exists in memory to avoid duplicates
        if not any(r.input_pattern == rule.input_pattern
                   for r in self.rules):
            self.rules.append(rule)

    def match_rule(self, user_input):
        # Implement rule matching logic here
        # Iterate through the rules and check if the user_input
        # matches any of the input_patterns using the match() method
        for rule in self.rules:
            if rule.match(user_input):
                return rule
        return None

    def update_rule(self, user_input, user_feedback):
        # Find the matching rule based on user input
        matching_rule = self.match_rule(user_input)
        if matching_rule:
            # Update the matching rule with user feedback
            matching_rule.update(user_input, user_feedback)
            # Update the rule in the RuleDB
            self.rule_db.update_rule(matching_rule)

    def load_rules_from_db(self):
        # Load rules from the RuleDB and populate the rules list
        self.rules = self.rule_db.get_rules()

    def process_message(self, user_input):
        # Implement message processing logic here
        # For example, you can call match_rule() to find the matching rule,
        # and return the corresponding output pattern from the matched rule.
        matching_rule = self.match_rule(user_input)
        if matching_rule:
            return matching_rule.output_pattern
        return None
