# CLAUDE.md - AI Assistant Guide for Eris

## Project Overview

**Eris** is a rule-based learning AI Discord bot created by Dani. The bot learns through a combination of predefined rules, user feedback, and continuous learning mechanisms. It interacts with users via Discord messages, processes input through a rule engine, and improves responses based on user reactions.

### Key Features
- Rule-based message processing with pattern matching
- SQLite database for persistent rule storage
- User feedback system (1-5 star ratings via Discord reactions)
- Continuous learning capabilities
- Autonomous rule generation

## Architecture & Structure

### File Structure
```
/home/user/Eris/
├── main.py                    # Discord bot entry point and event handlers
├── rule_engine.py             # Core rule matching and processing logic
├── rules.py                   # Predefined rule definitions
├── continuous_learning.py     # Learning system implementation
├── eris.db                    # SQLite database (auto-generated)
├── .env                       # Environment variables (gitignored)
├── readme.md                  # User-facing documentation
├── LICENSE                    # MIT License
├── Eris.png                   # Bot avatar/logo
└── .gitignore                 # Standard Python gitignore
```

### Core Components

#### 1. **main.py** - Discord Bot Entry Point
- **Purpose**: Initializes Discord client, loads environment variables, handles message events
- **Key Functions**:
  - `on_ready()`: Bot initialization confirmation (line 34)
  - `on_message()`: Main message handler with feedback loop (line 38)
- **Flow**:
  1. Receives Discord message
  2. Processes through RuleEngine first
  3. Falls back to ContinuousLearning if no rule matches
  4. Adds reaction emojis (1-5) for user feedback
  5. Waits 60 seconds for user reaction
  6. Updates rules based on feedback
- **Dependencies**: discord.py, dotenv, rule_engine, continuous_learning, rules

#### 2. **rule_engine.py** - Core Rule Processing
- **Classes**:
  - `Rule`: Represents a single input-output pattern pair
    - `match(user_input)`: Simple substring matching (line 9-13)
    - `update(user_input, user_feedback)`: Stub for rule updates (line 15-17)
  - `RuleDB`: SQLite database interface
    - `add_rule(rule)`: Inserts new rule, handles duplicates (line 29-36)
    - `update_rule(rule)`: Updates existing rule with timestamp (line 38-42)
    - `get_rules()`: Retrieves all rules from DB (line 44-53)
  - `RuleEngine`: Main processing engine
    - `match_rule(user_input)`: Finds first matching rule (line 66-73)
    - `process_message(user_input)`: Returns output for matched rule (line 88-94)
    - `update_rule(user_input, user_feedback)`: Updates rule based on feedback (line 75-82)

#### 3. **rules.py** - Rule Definitions
- **Classes**:
  - `Rules`: Simple data class for rule storage
- **Rule Categories**:
  - `original_rules`: Base greetings and responses (6 default rules)
  - `user_feedback_rules`: Rules learned from user feedback (empty initially)
  - `autonomous_rules`: Self-generated rules (empty initially)
  - `all_rules`: Combined list exported to main.py

#### 4. **continuous_learning.py** - Learning System
- **Class**: `ContinuousLearning`
- **Methods**:
  - `handle_user_input(user_input)`: Matches input and generates response (line 14-25)
  - `capture_user_feedback(user_input, user_feedback)`: Updates rules based on feedback (line 27-34)
  - `process_message(user_input, user_feedback=None)`: Main processing interface (line 38-45)
- **Default Response**: "I'm sorry, I didn't understand that." (when no rule matches)

## Database Schema

### Table: `rules`
```sql
CREATE TABLE rules (
    input_pattern TEXT PRIMARY KEY,
    output_pattern TEXT,
    last_changed TEXT
)
```

- **input_pattern**: Unique identifier, the text pattern to match against
- **output_pattern**: The bot's response when pattern matches
- **last_changed**: ISO timestamp of last modification

## Development Workflow

### Environment Setup

1. **Required Environment Variables** (stored in `.env`):
   - `DISCORD_TOKEN`: Discord bot authentication token
   - `DB_NAME`: SQLite database filename (default: `eris.db`)

2. **Dependencies**:
   - `discord.py`: Discord API wrapper
   - `python-dotenv`: Environment variable management
   - `sqlite3`: Built-in Python module

3. **Installation**:
   ```bash
   pip install discord.py python-dotenv
   ```

### Running the Bot
```bash
python main.py
```

## Key Conventions for AI Assistants

### Code Style
1. **Indentation**: 4 spaces (consistent throughout)
2. **Naming Conventions**:
   - Classes: PascalCase (`RuleEngine`, `ContinuousLearning`)
   - Functions/Methods: snake_case (`process_message`, `add_rule`)
   - Variables: snake_case (`user_input`, `matching_rule`)
3. **String Literals**: Double quotes for general strings
4. **Comments**: Inline comments for complex logic, docstrings not currently used

### Database Interactions
- Always use parameterized queries to prevent SQL injection
- Handle `sqlite3.IntegrityError` for duplicate rule prevention
- Commit after every write operation
- Store timestamps as ISO format strings via `datetime.datetime.now()`

### Error Handling
- **Current State**: Minimal error handling
- **Database**: Try-except for duplicate rules (rule_engine.py:31-36)
- **Discord Events**: Asyncio timeout handling for reactions (main.py:60-66)
- **Improvement Needed**: Add validation for user input, handle DB connection errors

### Rule Matching Logic
- **Current**: Simple substring matching (`input_pattern in user_input`)
- **Case Sensitive**: Yes
- **Partial Matches**: Supported
- **First Match Wins**: Engine returns first matching rule only

## Common Tasks for AI Assistants

### Adding New Rules
1. **Predefined Rules** (static, version controlled):
   - Add to `rules.py` in appropriate category
   - Example:
     ```python
     Rules("pattern", "response")
     ```

2. **Dynamic Rules** (runtime, stored in DB):
   - Bot automatically creates rules when it generates responses
   - See main.py:71-80 for autonomous rule creation logic

### Modifying Rule Matching Logic
- **Location**: `rule_engine.py`, `Rule.match()` method (line 9-13)
- **Current**: Substring matching
- **Enhancement Ideas**:
  - Implement regex pattern matching
  - Add fuzzy string matching (e.g., Levenshtein distance)
  - Case-insensitive matching
  - Word boundary detection

### Extending Learning Capabilities
- **Location**: `continuous_learning.py`
- **Current Limitation**: Simple rule updates based on feedback
- **Enhancement Ideas**:
  - Implement confidence scores
  - Track rule effectiveness over time
  - Implement rule decay for outdated patterns
  - Add natural language understanding (NLU)

### Database Modifications
- **Schema Changes**: Modify table creation in `rule_engine.py`, `RuleDB.__init__()` (line 25-27)
- **Migration**: No migration system currently - requires manual DB updates
- **Backup**: Not automated - recommend backing up `eris.db` before schema changes

## Code Patterns & Best Practices

### Discord Bot Patterns
1. **Message Filtering**: Always check if message author is bot itself (main.py:39-40)
2. **Reaction Feedback**: Use numbered emoji reactions for 1-5 scale feedback
3. **Async/Await**: All Discord event handlers are async
4. **Timeout Handling**: 60-second timeout for user reactions

### Rule Processing Pattern
```python
# Standard flow:
response = rule_engine.process_message(input)
if response is None:
    response = learning_engine.process_message(input)
```

### Database Connection Pattern
```python
# RuleDB maintains persistent connection
self.conn = sqlite3.connect(db_name)
self.cursor = self.conn.cursor()
# Remember to commit after writes
self.conn.commit()
```

## Security Considerations

### Current State
- **Environment Variables**: Discord token stored in `.env` (gitignored) ✓
- **SQL Injection**: Using parameterized queries ✓
- **Input Validation**: Minimal - no sanitization of user input ⚠
- **Rate Limiting**: Not implemented ⚠
- **Permissions**: Discord intents include members and message content

### Recommended Improvements
1. Add input length validation
2. Sanitize special characters in rule patterns
3. Implement rate limiting for rule creation
4. Add permission checks for sensitive operations
5. Validate Discord token format before use

## Testing & Debugging

### Current State
- No unit tests present
- No testing framework configured
- Manual testing via Discord required

### Testing Recommendations
1. **Unit Tests**:
   - Test rule matching logic independently
   - Test database operations with temporary DB
   - Mock Discord client for message handling tests

2. **Integration Tests**:
   - Test full message processing flow
   - Test feedback loop functionality
   - Test rule persistence across restarts

3. **Suggested Framework**: pytest
   ```bash
   pip install pytest pytest-asyncio
   ```

### Debugging Tips
1. **Database Inspection**:
   ```bash
   sqlite3 eris.db "SELECT * FROM rules;"
   ```

2. **Enable Discord.py Logging**:
   ```python
   import logging
   logging.basicConfig(level=logging.INFO)
   ```

3. **Rule Matching Issues**: Add debug prints in `Rule.match()` to see what patterns are tested

## Important Notes

### Behavior Quirks
1. **Double Rule Addition**: Rules are added to both RuleDB and RuleEngine (main.py:27-30)
   - This appears redundant as RuleEngine loads from RuleDB
   - May cause issues if not synchronized

2. **Self-Message Rule Creation**: Bot creates rules from its own messages (main.py:71-80)
   - Logic may never execute as message.author == client.user check happens earlier
   - Potential dead code or logic error

3. **Feedback Without Response**: Feedback is always processed even if response is None (main.py:69)
   - Could lead to updating non-existent rules

4. **First Match Only**: Rule engine stops at first match
   - Consider if multiple matching rules should influence response

### Known Limitations
1. **Simple Pattern Matching**: Only substring matching, no advanced NLP
2. **No Rule Priority**: First match wins, no weighting or confidence scores
3. **No Conversation Context**: Each message processed independently
4. **Single Response**: Bot only sends one message per user input
5. **Feedback Timeout**: Only 60 seconds to provide feedback

### Future Enhancement Areas
1. Implement proper NLP/NLU for intent recognition
2. Add conversation context/memory
3. Implement rule confidence scoring
4. Add analytics for rule effectiveness
5. Create admin commands for rule management
6. Implement rule versioning and rollback
7. Add multi-language support
8. Create web dashboard for rule management

## Quick Reference for AI Assistants

### When Modifying Code:
- ✓ Maintain async/await patterns for Discord handlers
- ✓ Use parameterized SQL queries
- ✓ Update both RuleDB and RuleEngine when adding rules
- ✓ Handle database commit() after modifications
- ✓ Test rule matching with various input patterns
- ✓ Consider case sensitivity in pattern matching
- ✓ Preserve the feedback loop mechanism

### When Adding Features:
- ✓ Consider database schema impact
- ✓ Maintain backward compatibility with existing rules
- ✓ Document new environment variables
- ✓ Update rules.py for new static rules
- ✓ Test with Discord bot before committing

### When Debugging:
- Check `eris.db` for actual rule content
- Verify `.env` file exists with correct tokens
- Review Discord bot permissions and intents
- Test rule matching logic independently
- Check for async/await syntax errors

---

**Last Updated**: 2025-11-14
**Maintained By**: AI Assistant
**Project Owner**: Dani (MystiaTech)
