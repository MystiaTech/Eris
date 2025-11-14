import asyncio
import os
import discord
from dotenv import load_dotenv
from continuous_learning import ContinuousLearning
from rule_engine import Rule, RuleEngine, RuleDB
from rules import all_rules  # Import all_rules from rules.py

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DB_NAME = os.getenv('DB_NAME')
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)

# Create an instance of RuleDB
rule_db = RuleDB(DB_NAME)

# Create an instance of ContinuousLearning module
learning_engine = ContinuousLearning(rule_db)

# Create an instance of RuleEngine
rule_engine = RuleEngine(rule_db)

# Add rules from all_rules into the database
for rule in all_rules:
    rule_db.add_rule(Rule(rule.input_pattern, rule.output_pattern))
    # Add rules from all_rules into the RuleEngine
    rule_engine.add_rule(Rule(rule.input_pattern, rule.output_pattern))


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Process the message and generate a response
    # using RuleEngine and ContinuousLearning
    response = rule_engine.process_message(message.content)
    if response is None:
        response = learning_engine.process_message(message.content)

    # Send the response back to the same channel
    response_message = await message.channel.send(response)

    # Add reactions for user feedback
    for i in range(1, 6):
        emoji_unicode = f'{i}\uFE0F\u20E3'
        await response_message.add_reaction(emoji_unicode)

    # Define a check function for reaction event
    def check(reaction, user):
        return (
            user == message.author and
            str(reaction.emoji) in
            [f'{i}\uFE0F\u20E3' for i in range(1, 6)] and
            reaction.message.id == response_message.id
        )

    # Wait for user reaction
    try:
        reaction, _ = await client.wait_for(
            'reaction_add', timeout=60.0, check=check
        )
        feedback = int(reaction.emoji[0])
        # Pass the feedback to ContinuousLearning for updating rules
        learning_engine.process_message(
            message.content, user_feedback=feedback
        )
    except asyncio.TimeoutError:
        feedback = None

    # Pass the feedback to the RuleEngine for updating rules
    rule_engine.update_rule(message.content, feedback)

    # Check if the message is from Eris herself and not a user
    if message.author == client.user:
        # Check if the response is not None, indicating that
        # Eris generated a response
        if response is not None:
            # Create a new rule with the input pattern as the
            # original message content and the output pattern as
            # the generated response
            new_rule = Rule(
                input_pattern=message.content,
                output_pattern=response
            )
            # Add the new rule to the RuleDB and RuleEngine
            rule_db.add_rule(new_rule)
            rule_engine.add_rule(new_rule)


client.run(TOKEN)
