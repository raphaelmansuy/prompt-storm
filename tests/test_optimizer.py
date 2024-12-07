"""Tests for the prompt optimizer module."""
import pytest
import warnings
from unittest.mock import patch, MagicMock
from prompt_storm.optimizer import PromptOptimizer, OptimizationConfig

class MockResponse:
    """Mock response for litellm completion calls."""
    def __init__(self, content):
        self.choices = [
            type('Choice', (), {'message': type('Message', (), {'content': content})})()
        ]

@pytest.fixture
def optimizer():
    """Create a default optimizer instance (using gpt-4o-mini)."""
    return PromptOptimizer()

@pytest.fixture
def custom_optimizer():
    """Create an optimizer with custom configuration, but maintaining gpt-4o-mini as model."""
    config = OptimizationConfig(
        model="gpt-4o-mini",  # Maintaining the required model
        temperature=0.5,
        max_tokens=1000,
        template="Optimize this prompt: {prompt}"
    )
    return PromptOptimizer(config)

def test_optimize_basic():
    """Test basic prompt optimization with gpt-4o-mini."""
    with patch('litellm.completion') as mock_completion:
        mock_completion.return_value = MockResponse('Mocked response')
        optimizer = PromptOptimizer()
        test_prompt = "Tell me about Python"
        result = optimizer.optimize(test_prompt)
        assert isinstance(result, str)
        assert len(result) > 0
        mock_completion.assert_called_once()

def test_optimizer_config():
    """Test optimizer configuration maintains gpt-4o-mini as model."""
    config = OptimizationConfig(temperature=0.5)  # Only changing temperature
    optimizer = PromptOptimizer(config)
    assert optimizer.config.model == "gpt-4o-mini"  # Ensuring model remains correct
    assert optimizer.config.temperature == 0.5

def test_optimize_with_custom_config():
    """Test optimization with custom configuration using gpt-4o-mini."""
    with patch('litellm.completion') as mock_completion:
        mock_completion.return_value = MockResponse('Mocked response')
        custom_optimizer = PromptOptimizer(OptimizationConfig(temperature=0.5))
        test_prompt = "Explain machine learning"
        result = custom_optimizer.optimize(test_prompt)
        assert isinstance(result, str)
        assert len(result) > 0
        mock_completion.assert_called_once()

def test_model_not_changed():
    """Specific test to ensure model cannot be changed from gpt-4o-mini."""
    config = OptimizationConfig()
    assert config.model == "gpt-4o-mini", "Default model must be gpt-4o-mini"
    
    # Even when creating with custom config, model should remain gpt-4o-mini
    custom_config = OptimizationConfig(temperature=0.1, max_tokens=500)
    assert custom_config.model == "gpt-4o-mini", "Model must remain gpt-4o-mini even with custom config"

def test_format_to_yaml_basic():
    """Test basic YAML formatting with default configuration."""
    with patch('litellm.completion') as mock_completion:
        mock_response = """
name: test_prompt
version: '1.0'
description: A test prompt
content: >-
  Test content
"""
        mock_completion.return_value = MockResponse(mock_response)
        optimizer = PromptOptimizer()
        result = optimizer.format_to_yaml("test prompt")
        assert isinstance(result, str)
        assert 'name:' in result
        assert 'version:' in result
        assert 'content:' in result
        mock_completion.assert_called_once()

def test_format_to_yaml_complex():
    """Test YAML formatting with a complex prompt containing variables."""
    with patch('litellm.completion') as mock_completion:
        mock_response = """
name: complex_prompt
version: '1.0'
variables:
  - name: user_name
    type: string
  - name: age
    type: integer
content: >-
  Hello {user_name}, you are {age} years old.
"""
        mock_completion.return_value = MockResponse(mock_response)
        optimizer = PromptOptimizer()
        result = optimizer.format_to_yaml("Hello {user_name}, you are {age} years old.")
        assert isinstance(result, str)
        assert 'variables:' in result
        assert 'user_name' in result
        assert 'age' in result
        mock_completion.assert_called_once()

def test_format_to_yaml_with_markdown_markers():
    """Test YAML formatting with markdown code block markers."""
    with patch('litellm.completion') as mock_completion:
        mock_response = """```yaml
name: test_prompt
version: '1.0'
content: Test content
```"""
        mock_completion.return_value = MockResponse(mock_response)
        optimizer = PromptOptimizer()
        result = optimizer.format_to_yaml("test prompt")
        assert isinstance(result, str)
        assert 'name:' in result
        assert 'version:' in result
        assert 'content:' in result
        assert '```' not in result  # Markdown markers should be stripped
        mock_completion.assert_called_once()

def test_format_to_yaml_without_markers():
    """Test YAML formatting when no markdown markers are present."""
    with patch('litellm.completion') as mock_completion:
        mock_response = """name: test_prompt
version: '1.0'
content: Test content"""
        mock_completion.return_value = MockResponse(mock_response)
        optimizer = PromptOptimizer()
        result = optimizer.format_to_yaml("test prompt")
        assert isinstance(result, str)
        assert 'name:' in result
        assert 'version:' in result
        mock_completion.assert_called_once()

def test_format_to_yaml_rate_limit_error():
    """Test handling of rate limit errors in YAML formatting."""
    with patch('litellm.completion') as mock_completion:
        mock_completion.side_effect = Exception("Rate limit exceeded")
        optimizer = PromptOptimizer()
        with pytest.raises(Exception) as exc_info:
            optimizer.format_to_yaml("test prompt")
        assert "Rate limit exceeded" in str(exc_info.value)
