# Eris - Rule/Learning AI
![Eris](/Eris.png)

Hello, I am Eris, a simple Learning Ai, created by Dani. I currently learn via rules but Dani is working on making smarter

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy the example environment file and edit it with your Discord bot token:
```bash
cp .env.example .env
# Edit .env and add your DISCORD_TOKEN
```

### 3. Run the Bot
```bash
python main.py
```

### 4. Test Functionality (Optional)
To verify the core functionality works without Discord:
```bash
python test_functionality.py
```

## Features
- Rule-based message processing with pattern matching
- SQLite database for persistent rule storage
- User feedback system (1-5 star ratings via Discord reactions)
- Continuous learning capabilities
- Autonomous rule generation

## Authors
- Dani (MystiaTech) - Original creator
- Claude (Anthropic) - Code improvements and PEP8 compliance
