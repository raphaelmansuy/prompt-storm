"""
Tests for the CLI functionality.
"""
import os
import tempfile
from click.testing import CliRunner
import pytest
from prompt_storm.cli import cli, optimize
from prompt_storm.optimizer import PromptOptimizer

@pytest.fixture
def runner():
    """Create a CLI test runner."""
    return CliRunner()

@pytest.fixture
def mock_optimizer(mocker):
    """Mock the optimizer to avoid actual API calls."""
    mock = mocker.patch('prompt_storm.cli.PromptOptimizer', autospec=True)
    instance = mock.return_value
    instance.optimize.return_value = "Optimized: Test prompt"
    return mock

def test_cli_exists(runner):
    """Test that the CLI command group exists."""
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Prompt Storm CLI' in result.output

def test_optimize_command_exists(runner):
    """Test that the optimize command exists and shows help."""
    result = runner.invoke(cli, ['optimize', '--help'])
    assert result.exit_code == 0
    assert 'Optimize a prompt using LLM' in result.output

def test_optimize_basic(runner, mock_optimizer):
    """Test basic prompt optimization."""
    result = runner.invoke(cli, ['optimize', 'Test prompt'])
    assert result.exit_code == 0
    mock_optimizer.assert_called_once()
    mock_optimizer.return_value.optimize.assert_called_once_with('Test prompt')

def test_optimize_with_model(runner, mock_optimizer):
    """Test optimization with custom model."""
    result = runner.invoke(cli, ['optimize', '--model', 'gpt-3.5-turbo', 'Test prompt'])
    assert result.exit_code == 0
    mock_optimizer.assert_called_once()
    assert mock_optimizer.call_args[0][0].model == 'gpt-3.5-turbo'

def test_optimize_with_max_tokens(runner, mock_optimizer):
    """Test optimization with custom max tokens."""
    result = runner.invoke(cli, ['optimize', '--max-tokens', '1000', 'Test prompt'])
    assert result.exit_code == 0
    mock_optimizer.assert_called_once()
    assert mock_optimizer.call_args[0][0].max_tokens == 1000

def test_optimize_with_temperature(runner, mock_optimizer):
    """Test optimization with custom temperature."""
    result = runner.invoke(cli, ['optimize', '--temperature', '0.8', 'Test prompt'])
    assert result.exit_code == 0
    mock_optimizer.assert_called_once()
    assert mock_optimizer.call_args[0][0].temperature == 0.8

def test_optimize_from_file(runner, mock_optimizer):
    """Test optimization from input file."""
    with runner.isolated_filesystem():
        with open('input.txt', 'w', encoding='utf-8') as f:
            f.write('Test prompt from file')
        
        result = runner.invoke(cli, ['optimize', '--input-file', 'input.txt', 'ignored prompt'])
        assert result.exit_code == 0
        mock_optimizer.return_value.optimize.assert_called_once_with('Test prompt from file')

def test_optimize_to_file(runner, mock_optimizer):
    """Test optimization with output to file."""
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['optimize', '--output-file', 'output.txt', 'Test prompt'])
        assert result.exit_code == 0
        
        with open('output.txt', encoding='utf-8') as f:
            content = f.read()
        assert content == 'Optimized: Test prompt'

def test_optimize_error_handling(runner, mock_optimizer):
    """Test error handling in optimization."""
    mock_optimizer.return_value.optimize.side_effect = Exception('Test error')
    result = runner.invoke(cli, ['optimize', 'Test prompt'])
    assert result.exit_code == 1
    assert 'Error: Test error' in result.output

def test_optimize_invalid_temperature(runner, mock_optimizer):
    """Test validation of temperature parameter."""
    result = runner.invoke(cli, ['optimize', '--temperature', '2.0', 'Test prompt'])
    assert result.exit_code == 2  # Click's error exit code
    assert 'Invalid value' in result.output

def test_optimize_invalid_max_tokens(runner, mock_optimizer):
    """Test validation of max_tokens parameter."""
    result = runner.invoke(cli, ['optimize', '--max-tokens', '-1', 'Test prompt'])
    assert result.exit_code == 2
    assert 'Invalid value' in result.output

def test_optimize_missing_input_file(runner, mock_optimizer):
    """Test error handling for missing input file."""
    result = runner.invoke(cli, ['optimize', '--input-file', 'nonexistent.txt', 'Test prompt'])
    assert result.exit_code == 2
    assert 'does not exist' in result.output
