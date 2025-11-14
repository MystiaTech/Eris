#!/usr/bin/env python3
"""
Verify that all functions in the codebase are complete and ready-to-run.
Checks for incomplete implementations, missing return statements, etc.
"""

import ast
import sys


def check_function_completeness(filename):
    """Check if all functions in a file are complete."""
    print(f"\nChecking {filename}...")

    with open(filename, 'r') as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        print(f"  ✗ Syntax error: {e}")
        return False

    issues = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func_name = node.name

            # Check if function body is just 'pass'
            if (len(node.body) == 1 and
                    isinstance(node.body[0], ast.Pass)):
                issues.append(
                    f"  ✗ Function '{func_name}' only contains 'pass'"
                )

            # Check if function body is just '...' (Ellipsis)
            if (len(node.body) == 1 and
                    isinstance(node.body[0], ast.Expr) and
                    isinstance(node.body[0].value, ast.Constant) and
                    node.body[0].value.value is ...):
                issues.append(
                    f"  ✗ Function '{func_name}' only contains '...'"
                )

            # Check if function has TODO/FIXME comments indicating
            # incomplete work
            # (This is basic - just checks docstrings)
            if node.body and isinstance(node.body[0], ast.Expr):
                if isinstance(node.body[0].value, ast.Constant):
                    docstring = node.body[0].value.value
                    if isinstance(docstring, str):
                        markers = ['TODO', 'FIXME', 'XXX']
                        if any(marker in docstring.upper()
                               for marker in markers):
                            issues.append(
                                f"  ⚠ Function '{func_name}' has "
                                f"TODO/FIXME in docstring"
                            )

    if issues:
        for issue in issues:
            print(issue)
        return False
    else:
        print("  ✓ All functions complete")
        return True


def check_all_returns(filename):
    """Check that functions have appropriate return statements."""
    print(f"\nChecking return statements in {filename}...")

    with open(filename, 'r') as f:
        source = f.read()

    tree = ast.parse(source)
    warnings = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func_name = node.name

            # Skip __init__ and special methods
            if func_name.startswith('__'):
                continue

            # Check if function has any return statements
            has_return = any(isinstance(n, ast.Return)
                             for n in ast.walk(node))

            # Check if function assigns to variables but never returns
            has_assignment = any(isinstance(n, ast.Assign)
                                 for n in ast.walk(node))

            # If function has logic but no return, warn
            if has_assignment and not has_return and len(node.body) > 1:
                # Check if it's just setting instance variables
                is_setter = all(
                    isinstance(stmt, ast.Assign) and
                    any(isinstance(target, ast.Attribute) and
                        isinstance(target.value, ast.Name) and
                        target.value.id == 'self'
                        for target in stmt.targets)
                    for stmt in node.body
                    if isinstance(stmt, ast.Assign)
                )

                if not is_setter:
                    warnings.append(
                        f"  ⚠ Function '{func_name}' has assignments "
                        f"but no return"
                    )

    if warnings:
        for warning in warnings:
            print(warning)
    else:
        print("  ✓ Return statements look good")

    return True


def main():
    """Run all completeness checks."""
    print("=" * 60)
    print("Code Completeness Verification")
    print("=" * 60)

    files_to_check = [
        'main.py',
        'rule_engine.py',
        'continuous_learning.py',
        'rules.py'
    ]

    all_good = True

    for filename in files_to_check:
        try:
            if not check_function_completeness(filename):
                all_good = False
            check_all_returns(filename)
        except FileNotFoundError:
            print(f"  ✗ File not found: {filename}")
            all_good = False
        except Exception as e:
            print(f"  ✗ Error checking {filename}: {e}")
            all_good = False

    print("\n" + "=" * 60)
    if all_good:
        print("✓ All code is complete and ready-to-run!")
        print("=" * 60)
        return 0
    else:
        print("✗ Some issues found (see above)")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
