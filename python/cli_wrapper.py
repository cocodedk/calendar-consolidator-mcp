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

    args = parser.parse_args()

    try:
        # Import module
        module = importlib.import_module(args.module)

        # Get function
        func = getattr(module, args.function)

        # Parse parameters
        params = json.loads(args.params)

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
