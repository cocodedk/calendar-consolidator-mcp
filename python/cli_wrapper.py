#!/usr/bin/env python3
"""
CLI wrapper for Python functions.
Allows Node.js to call Python functions via command line.
"""

import sys
import json
import argparse
import importlib


def main():
    """Parse arguments and execute Python function."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--module', required=True, help='Python module path')
    parser.add_argument('--function', required=True, help='Function name')
    parser.add_argument('--params', required=True, help='JSON parameters')
    parser.add_argument('--class', dest='class_name', help='Class name (if calling class method)')

    args = parser.parse_args()

    try:
        # Import module
        module = importlib.import_module(args.module)

        # Parse parameters
        params = json.loads(args.params)

        # Check if calling a class method
        if args.class_name:
            # Get class and instantiate it
            cls = getattr(module, args.class_name)
            instance = cls()
            # Get method from instance
            func = getattr(instance, args.function)
        else:
            # Get function directly from module
            func = getattr(module, args.function)

        # Call function
        result = func(**params)

        # Output result as JSON
        print(json.dumps(result))

    except Exception as e:
        error = {
            'error': str(e),
            'type': type(e).__name__
        }
        print(json.dumps(error), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
