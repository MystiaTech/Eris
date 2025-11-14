#!/usr/bin/env python3
"""
Test script to verify Eris core functionality works correctly.
This tests the rule engine and learning system without Discord.
"""

import os
from rule_engine import Rule, RuleDB, RuleEngine
from continuous_learning import ContinuousLearning
from rules import all_rules


def cleanup_test_db():
    """Remove test database if it exists."""
    if os.path.exists('test_eris.db'):
        os.remove('test_eris.db')


def test_rule_creation():
    """Test creating rules."""
    print("Test 1: Rule Creation")
    rule = Rule("hello", "Hi there!")
    assert rule.input_pattern == "hello"
    assert rule.output_pattern == "Hi there!"
    print("  ✓ Rule creation works")


def test_rule_matching():
    """Test rule matching logic."""
    print("\nTest 2: Rule Matching")
    rule = Rule("hello", "Hi there!")

    # Test positive match
    assert rule.match("hello") is True
    assert rule.match("hello world") is True
    print("  ✓ Positive matching works")

    # Test negative match
    assert rule.match("goodbye") is False
    print("  ✓ Negative matching works")


def test_rule_database():
    """Test database operations."""
    print("\nTest 3: Database Operations")
    cleanup_test_db()

    db = RuleDB('test_eris.db')

    # Test adding rule
    rule1 = Rule("test", "response")
    db.add_rule(rule1)
    print("  ✓ Adding rule works")

    # Test retrieving rules
    rules = db.get_rules()
    assert len(rules) == 1
    assert rules[0].input_pattern == "test"
    assert rules[0].output_pattern == "response"
    print("  ✓ Retrieving rules works")

    # Test adding duplicate (should not crash)
    db.add_rule(rule1)
    rules = db.get_rules()
    assert len(rules) == 1
    print("  ✓ Duplicate handling works")

    # Test updating rule
    rule1.output_pattern = "new response"
    db.update_rule(rule1)
    rules = db.get_rules()
    assert rules[0].output_pattern == "new response"
    print("  ✓ Updating rules works")

    cleanup_test_db()


def test_rule_engine():
    """Test rule engine functionality."""
    print("\nTest 4: Rule Engine")
    cleanup_test_db()

    db = RuleDB('test_eris.db')
    engine = RuleEngine(db)

    # Add some rules
    engine.add_rule(Rule("hello", "Hi there!"))
    engine.add_rule(Rule("bye", "Goodbye!"))

    # Test matching
    response = engine.process_message("hello world")
    assert response == "Hi there!"
    print("  ✓ Message processing works")

    # Test no match
    response = engine.process_message("unknown input")
    assert response is None
    print("  ✓ No match returns None")

    cleanup_test_db()


def test_continuous_learning():
    """Test continuous learning functionality."""
    print("\nTest 5: Continuous Learning")
    cleanup_test_db()

    db = RuleDB('test_eris.db')
    learning = ContinuousLearning(db)

    # Add initial rules
    learning.rule_engine.add_rule(Rule("hello", "Hi!"))

    # Test matching existing rule
    response = learning.process_message("hello")
    assert response == "Hi!"
    print("  ✓ Learning engine processes known input")

    # Test unknown input (should return default message)
    response = learning.process_message("unknown")
    assert response == "I'm sorry, I didn't understand that."
    print("  ✓ Learning engine handles unknown input")

    cleanup_test_db()


def test_predefined_rules():
    """Test that predefined rules are loaded."""
    print("\nTest 6: Predefined Rules")
    assert len(all_rules) > 0
    print(f"  ✓ Found {len(all_rules)} predefined rules")

    # Check rule structure
    for rule in all_rules:
        assert hasattr(rule, 'input_pattern')
        assert hasattr(rule, 'output_pattern')
    print("  ✓ All rules have correct structure")


def test_integration():
    """Test full integration of components."""
    print("\nTest 7: Integration Test")
    cleanup_test_db()

    # Setup
    db = RuleDB('test_eris.db')
    engine = RuleEngine(db)
    learning = ContinuousLearning(db)

    # Add rules from all_rules
    for rule in all_rules:
        engine.add_rule(Rule(rule.input_pattern, rule.output_pattern))

    # Test processing through engine
    response = engine.process_message("hello")
    assert response is not None
    print("  ✓ Engine processes predefined rules")

    # Test fallback to learning engine
    response = engine.process_message("unknown input")
    if response is None:
        response = learning.process_message("unknown input")
    assert response == "I'm sorry, I didn't understand that."
    print("  ✓ Fallback to learning engine works")

    cleanup_test_db()


def main():
    """Run all tests."""
    print("=" * 50)
    print("Eris Functionality Tests")
    print("=" * 50)

    try:
        test_rule_creation()
        test_rule_matching()
        test_rule_database()
        test_rule_engine()
        test_continuous_learning()
        test_predefined_rules()
        test_integration()

        print("\n" + "=" * 50)
        print("✓ All tests passed!")
        print("=" * 50)
        return 0

    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        cleanup_test_db()


if __name__ == "__main__":
    exit(main())
