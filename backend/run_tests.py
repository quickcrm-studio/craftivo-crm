#!/usr/bin/env python
"""
Script to run tests with coverage reporting.
"""

import os
import sys
import subprocess
import argparse

def run_tests(app_names=None, verbosity=1, failfast=False, with_coverage=True):
    """
    Run Django tests with coverage reporting.
    
    Args:
        app_names: List of app names to test (None for all apps)
        verbosity: Test verbosity level (1-3)
        failfast: Stop tests on first failure
        with_coverage: Whether to run tests with coverage
    
    Returns:
        Exit code from the test command
    """
    # Construct the test command
    if with_coverage:
        cmd = [
            'coverage', 'run', '--source=.',
            'manage.py', 'test'
        ]
    else:
        cmd = ['python', 'manage.py', 'test']
    
    # Add app names if specified
    if app_names:
        cmd.extend(app_names)
    
    # Add verbosity
    cmd.extend(['--verbosity', str(verbosity)])
    
    # Add failfast if specified
    if failfast:
        cmd.append('--failfast')
    
    # Run the tests
    test_result = subprocess.run(cmd)
    
    # Generate coverage report if using coverage
    if with_coverage and test_result.returncode == 0:
        print("\nGenerating coverage report...")
        subprocess.run(['coverage', 'report'])
        # Generate HTML report
        subprocess.run(['coverage', 'html'])
        print("\nHTML coverage report generated in htmlcov/index.html")
    
    return test_result.returncode

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run Django tests with coverage.')
    parser.add_argument('apps', nargs='*', help='App names to test (default: all)')
    parser.add_argument('-v', '--verbosity', type=int, choices=[0, 1, 2, 3], default=1,
                        help='Test verbosity level (default: 1)')
    parser.add_argument('-f', '--failfast', action='store_true',
                        help='Stop tests on first failure')
    parser.add_argument('--no-coverage', action='store_true',
                        help='Run tests without coverage')
    
    args = parser.parse_args()
    
    # Run the tests
    exit_code = run_tests(
        app_names=args.apps,
        verbosity=args.verbosity,
        failfast=args.failfast,
        with_coverage=not args.no_coverage
    )
    
    # Exit with the test command's exit code
    sys.exit(exit_code) 