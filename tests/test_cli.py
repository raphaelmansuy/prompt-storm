"""
Tests for the CLI module.
"""
import os
import tempfile
from unittest.mock import patch, MagicMock
import pytest
from click.testing import CliRunner
from prompt_storm.cli import cli, optimize
from prompt_storm.optimizer import PromptOptimizer

@pytest.fixture
def runner():
    """Create a CLI runner."""
    return CliRunner()

@pytest.fixture
def mock_optimizer():
    """Create a mock optimizer."""
    with patch('prompt_storm.optimizer.PromptOptimizer.optimize') as mock_opt:
        mock_opt.return_value = "Optimized: Test prompt"
        yield mock_opt

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

def test_optimize_basic(runner):
    """Test basic prompt optimization."""
    with patch('prompt_storm.optimizer.PromptOptimizer.optimize') as mock_optimize:
        mock_optimize.return_value = "Optimized prompt"
        result = runner.invoke(cli, ['optimize', 'Test prompt'])
        assert result.exit_code == 0
        assert "Optimized prompt" in result.output
        mock_optimize.assert_called_once_with("Test prompt")

def test_optimize_with_model(runner):
    """Test optimization with custom model."""
    with patch('prompt_storm.optimizer.PromptOptimizer.optimize') as mock_optimize:
        mock_optimize.return_value = "Optimized prompt"
        result = runner.invoke(cli, ['optimize', '--model', 'gpt-3.5-turbo', 'Test prompt'])
        assert result.exit_code == 0
        assert "Optimized prompt" in result.output
        mock_optimize.assert_called_once_with("Test prompt")

def test_optimize_with_max_tokens(runner):
    """Test optimization with custom max tokens."""
    with patch('prompt_storm.optimizer.PromptOptimizer.optimize') as mock_optimize:
        mock_optimize.return_value = "Optimized prompt"
        result = runner.invoke(cli, ['optimize', '--max-tokens', '1000', 'Test prompt'])
        assert result.exit_code == 0
        assert "Optimized prompt" in result.output
        mock_optimize.assert_called_once_with("Test prompt")

def test_optimize_with_temperature(runner):
    """Test optimization with custom temperature."""
    with patch('prompt_storm.optimizer.PromptOptimizer.optimize') as mock_optimize:
        mock_optimize.return_value = "Optimized prompt"
        result = runner.invoke(cli, ['optimize', '--temperature', '0.8', 'Test prompt'])
        assert result.exit_code == 0
        assert "Optimized prompt" in result.output
        mock_optimize.assert_called_once_with("Test prompt")

def test_optimize_from_file(runner):
    """Test optimization from input file."""
    with patch('prompt_storm.optimizer.PromptOptimizer.optimize') as mock_optimize:
        mock_optimize.return_value = "Optimized prompt"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write("Test prompt from file")
            tmp.flush()
            
            result = runner.invoke(cli, ['optimize', '--input-file', tmp.name, 'ignored prompt'])
            assert result.exit_code == 0
            assert "Optimized prompt" in result.output
            mock_optimize.assert_called_once_with("Test prompt from file")
            
            # Clean up
            os.unlink(tmp.name)

def test_optimize_to_file(runner):
    """Test optimization with output to file."""
    with patch('prompt_storm.optimizer.PromptOptimizer.optimize') as mock_optimize:
        mock_optimize.return_value = "Optimized prompt"
        
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            result = runner.invoke(cli, ['optimize', '--output-file', tmp.name, 'Test prompt'])
            assert result.exit_code == 0
            
            # Check file content
            with open(tmp.name, 'r') as f:
                content = f.read()
            assert "Optimized prompt" in content
            
            # Clean up
            os.unlink(tmp.name)

def test_optimize_error_handling(runner):
    """Test error handling in optimization."""
    with patch('prompt_storm.optimizer.PromptOptimizer.optimize') as mock_optimize:
        mock_optimize.side_effect = Exception("Test error")
        result = runner.invoke(cli, ['optimize', 'Test prompt'])
        assert result.exit_code == 1
        assert "Error: Test error" in result.output

def test_optimize_invalid_temperature(runner):
    """Test validation of temperature parameter."""
    result = runner.invoke(cli, ['optimize', '--temperature', '2.0', 'Test prompt'])
    assert result.exit_code == 2  # Click's error exit code
    assert 'Invalid value' in result.output

def test_optimize_invalid_max_tokens(runner):
    """Test validation of max_tokens parameter."""
    result = runner.invoke(cli, ['optimize', '--max-tokens', '-1', 'Test prompt'])
    assert result.exit_code == 2
    assert 'Invalid value' in result.output

def test_optimize_missing_input_file(runner):
    """Test error handling for missing input file."""
    result = runner.invoke(cli, ['optimize', '--input-file', 'nonexistent.txt', 'Test prompt'])
    assert result.exit_code == 2
    assert 'does not exist' in result.output

def test_optimize_with_yaml(runner):
    """Test prompt optimization with YAML formatting."""
    with patch('prompt_storm.optimizer.PromptOptimizer.optimize') as mock_optimize, \
         patch('prompt_storm.optimizer.PromptOptimizer.format_to_yaml') as mock_yaml:
        mock_optimize.return_value = "Optimized prompt"
        mock_yaml.return_value = "yaml: content"
        result = runner.invoke(cli, ['optimize', 'Test prompt', '--yaml'])
        assert result.exit_code == 0
        assert "yaml: content" in result.output
        mock_optimize.assert_called_once_with("Test prompt")
        mock_yaml.assert_called_once_with("Optimized prompt")

def test_optimize_with_yaml_and_file(runner):
    """Test prompt optimization with YAML formatting and file output."""
    with patch('prompt_storm.optimizer.PromptOptimizer.optimize') as mock_optimize, \
         patch('prompt_storm.optimizer.PromptOptimizer.format_to_yaml') as mock_yaml:
        mock_optimize.return_value = "Optimized prompt"
        mock_yaml.return_value = "yaml: content"
        
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            result = runner.invoke(cli, ['optimize', 'Test prompt', '--yaml', '-o', tmp.name])
            assert result.exit_code == 0
            
            # Check file content
            with open(tmp.name, 'r') as f:
                content = f.read()
            assert "yaml: content" in content
            
            # Clean up
            os.unlink(tmp.name)

def test_optimize_with_custom_config(runner):
    """Test optimization with custom configuration."""
    with patch('prompt_storm.optimizer.PromptOptimizer.optimize') as mock_optimize:
        mock_optimize.return_value = "Optimized prompt"
        result = runner.invoke(cli, [
            'optimize',
            'Test prompt',
            '--model', 'gpt-4o-mini',
            '--temperature', '0.5',
            '--max-tokens', '1000'
        ])
        assert result.exit_code == 0
        assert "Optimized prompt" in result.output

def test_optimize_with_input_file(runner):
    """Test optimization with input file."""
    with patch('prompt_storm.optimizer.PromptOptimizer.optimize') as mock_optimize:
        mock_optimize.return_value = "Optimized prompt"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write("Test prompt from file")
            tmp.flush()
            
            result = runner.invoke(cli, ['optimize', 'ignored', '-i', tmp.name])
            assert result.exit_code == 0
            assert "Optimized prompt" in result.output
            mock_optimize.assert_called_once_with("Test prompt from file")
            
            # Clean up
            os.unlink(tmp.name)
