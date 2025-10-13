"""Test CLI wrapper for Python function calls."""

import pytest
import json
import sys
from io import StringIO
from unittest.mock import patch, Mock
from python import cli_wrapper


def test_cli_wrapper_parses_arguments():
    """CLI wrapper parses module, function, and params."""
    test_args = [
        'cli_wrapper.py',
        '--module', 'test.module',
        '--function', 'test_func',
        '--params', '{"arg1": "value1"}'
    ]

    with patch('sys.argv', test_args):
        with patch('python.cli_wrapper.importlib.import_module'):
            with pytest.raises(SystemExit):
                cli_wrapper.main()


def test_cli_wrapper_calls_function():
    """CLI wrapper calls the specified function with params."""
    test_args = ['cli_wrapper.py', '--module', 'test.module', '--function', 'test_func', '--params', '{"arg1": "value1"}']
    
    with patch('sys.argv', test_args):
        with patch('python.cli_wrapper.importlib.import_module') as mock_import:
            mock_module = Mock()
            mock_func = Mock(return_value={'result': 'success'})
            mock_module.test_func = mock_func
            mock_import.return_value = mock_module

            # Capture stdout
            captured_output = StringIO()
            with patch('sys.stdout', captured_output):
                cli_wrapper.main()
                
            mock_func.assert_called_once_with(arg1="value1")
            # Verify JSON output
            output = captured_output.getvalue()
            result = json.loads(output)
            assert result['result'] == 'success'


def test_cli_wrapper_handles_exception():
    """CLI wrapper outputs error JSON on exception."""
    test_args = ['cli_wrapper.py', '--module', 'nonexistent.module', '--function', 'test_func', '--params', '{}']
    
    with patch('sys.argv', test_args):
        with patch('python.cli_wrapper.importlib.import_module') as mock_import:
            mock_import.side_effect = ModuleNotFoundError("Module not found")

            # Capture stderr
            captured_error = StringIO()
            with patch('sys.stderr', captured_error):
                with pytest.raises(SystemExit) as exc_info:
                    cli_wrapper.main()
                    
            assert exc_info.value.code == 1
            # Verify error was printed to stderr
            error_output = captured_error.getvalue()
            error_data = json.loads(error_output)
            assert 'error' in error_data
            assert error_data['type'] == 'ModuleNotFoundError'


def test_cli_wrapper_requires_all_arguments():
    """CLI wrapper requires module, function, and params."""
    incomplete_args = [
        'cli_wrapper.py',
        '--module', 'test.module'
    ]

    with patch('sys.argv', incomplete_args):
        with pytest.raises(SystemExit) as exc_info:
            cli_wrapper.main()
        # argparse exits with code 2 for missing arguments
        assert exc_info.value.code == 2
