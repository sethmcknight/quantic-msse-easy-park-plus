#!/usr/bin/env python3
"""
Test runner for the parking management system.

This script runs all tests with proper GUI mocking to prevent hanging issues.
"""

import sys
import os
import unittest
from unittest.mock import MagicMock

def setup_test_environment():
    """Set up the test environment with GUI mocking."""
    # Add src directory to Python path
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    # Mock tkinter modules to prevent GUI initialization during testing
    if 'tkinter' not in sys.modules:
        sys.modules['tkinter'] = MagicMock()
    if 'tkinter.ttk' not in sys.modules:
        sys.modules['tkinter.ttk'] = MagicMock()
    if 'tkinter.messagebox' not in sys.modules:
        sys.modules['tkinter.messagebox'] = MagicMock()

def run_tests():
    """Run all tests in the test suite."""
    setup_test_environment()
    
    # Change to src directory for proper imports
    original_cwd = os.getcwd()
    src_dir = os.path.join(os.path.dirname(__file__), 'src')
    os.chdir(src_dir)
    
    try:
        # Discover and run all tests
        loader = unittest.TestLoader()
        start_dir = 'tests'
        suite = loader.discover(start_dir, pattern='test_*.py')
        
        # Run tests with detailed output
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        # Print summary
        print(f"\n{'='*50}")
        print(f"Test Results Summary:")
        print(f"Tests run: {result.testsRun}")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        
        if result.wasSuccessful():
            print("✅ All tests passed!")
            return 0
        else:
            print("❌ Some tests failed!")
            
            if result.failures:
                print(f"\nFailures ({len(result.failures)}):")
                for test, tb_text in result.failures: # Renamed traceback to tb_text
                    print(f"  - Test: {test}")
                    print(f"    Traceback:\\n{tb_text}") # Print the traceback
                    
            if result.errors:
                print(f"\nErrors ({len(result.errors)}):")
                for test, tb_text in result.errors: # Renamed traceback to tb_text
                    print(f"  - Test: {test}")
                    print(f"    Traceback:\\n{tb_text}") # Print the traceback
            
            return 1
            
    finally:
        # Restore original working directory
        os.chdir(original_cwd)

def run_specific_test(test_name: str): # Added type hint for test_name
    """Run a specific test class or module."""
    setup_test_environment()
    
    # Change to src directory for proper imports
    original_cwd = os.getcwd()
    src_dir = os.path.join(os.path.dirname(__file__), 'src')
    os.chdir(src_dir)
    
    try:
        # Load and run specific test
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromName(test_name)
        
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return 0 if result.wasSuccessful() else 1
        
    finally:
        os.chdir(original_cwd)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Run specific test
        test_name = sys.argv[1]
        print(f"Running specific test: {test_name}")
        exit_code = run_specific_test(test_name)
    else:
        # Run all tests
        print("Running all tests...")
        exit_code = run_tests()
    
    sys.exit(exit_code)
