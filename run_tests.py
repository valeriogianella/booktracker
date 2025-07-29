#!/usr/bin/env python3
"""
Unified test runner for Booktrack application.
This replaces the separate test_core.py file.
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Run tests based on command line arguments."""
    if len(sys.argv) > 1 and sys.argv[1] == '--unittest':
        # Run unittest suite
        import unittest
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))
        
        # Discover and run tests
        loader = unittest.TestLoader()
        start_dir = os.path.join(os.path.dirname(__file__), 'tests')
        suite = loader.discover(start_dir)
        
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return 0 if result.wasSuccessful() else 1
    else:
        # Run standalone tests (default behavior)
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))
        
        try:
            # Import and run the standalone tests
            import test_booktrack
            test_booktrack.run_standalone_tests()
            return 0
        except Exception as e:
            print(f"❌ Test failed: {e}")
            return 1

if __name__ == '__main__':
    print("📋 Booktrack Test Runner")
    print("=" * 30)
    print("Usage:")
    print("  python run_tests.py           # Run standalone tests (recommended)")
    print("  python run_tests.py --unittest # Run unittest suite")
    print()
    
    sys.exit(main())
