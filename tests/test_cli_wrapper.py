"""Test CLI wrapper for Python function calls."""

import pytest
import json
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


@patch('python.cli_wrapper.importlib.import_module')
def test_cli_wrapper_calls_function(mock_import):
    """CLI wrapper calls the specified function with params."""
    mock_module = Mock()
    mock_func = Mock(return_value={'result': 'success'})
    mock_module.test_func = mock_func
    mock_import.return_value = mock_module

    test_args = [
        'cli_wrapper.py',
        '--module', 'test.module',
        '--function', 'test_func',
        '--params', '{"arg1": "value1"}'
    ]

    with patch('sys.argv', test_args):
        with patch('builtins.print') as mock_print:
            try:
                cli_wrapper.main()
            except SystemExit:
                pass  # main() calls sys.exit on success
            mock_func.assert_called_once_with(arg1="value1")
            # Verify JSON output
            if mock_print.call_count > 0:
                call_args = mock_print.call_args[0][0]
                result = json.loads(call_args)
                assert result['result'] == 'success'


@patch('python.cli_wrapper.importlib.import_module')
def test_cli_wrapper_handles_exception(mock_import):
    """CLI wrapper outputs error JSON on exception."""
    mock_import.side_effect = ModuleNotFoundError("Module not found")

    test_args = [
        'cli_wrapper.py',
        '--module', 'nonexistent.module',
        '--function', 'test_func',
        '--params', '{}'
    ]

    with patch('sys.argv', test_args):
        with patch('builtins.print'):  # Suppress error output
            with pytest.raises(SystemExit) as exc_info:
                cli_wrapper.main()
            assert exc_info.value.code == 1


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
