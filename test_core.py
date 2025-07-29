"""
DEPRECATED: This file has been unified into tests/test_booktrack.py

Please use one of these commands instead:

# Run all unittest tests:
python -m unittest tests.test_booktrack

# Run standalone tests (similar to this old file):
python tests/test_booktrack.py --standalone

# Or use the test runner:
python run_tests.py
"""

import sys
import os

# Redirect to the unified test file
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))

def main():
    print("⚠️  DEPRECATED: test_core.py has been unified into tests/test_booktrack.py")
    print()
    print("Please run tests using one of these commands:")
    print("  python -m unittest tests.test_booktrack")
    print("  python tests/test_booktrack.py --standalone")
    print("  python run_tests.py")
    print()
    
    # Ask user if they want to run the new tests
    try:
        response = input("Run the unified tests now? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            from test_booktrack import run_standalone_tests
            run_standalone_tests()
            return 0
        else:
            print("Tests not run. Use the commands above to run tests manually.")
            return 0
    except KeyboardInterrupt:
        print("\nTests cancelled.")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        print("Please run: python tests/test_booktrack.py --standalone")
        return 1

if __name__ == "__main__":
    exit(main())
