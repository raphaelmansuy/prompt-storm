"""Tests for the prompt optimizer module."""
import pytest
import asyncio
import warnings
from unittest.mock import patch, AsyncMock, MagicMock
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

def test_deprecated_optimize_async():
    """Test deprecated async compatibility method with gpt-4o-mini."""
    with patch('litellm.completion') as mock_completion:
        mock_completion.return_value = MockResponse('Mocked response')
        optimizer = PromptOptimizer()
        test_prompt = "What is AI?"
        with pytest.warns(DeprecationWarning):
            result = optimizer.optimize_async(test_prompt)
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

@pytest.mark.asyncio
async def test_aoptimize_basic():
    """Test basic async prompt optimization."""
    with patch('litellm.acompletion', new_callable=AsyncMock) as mock_acompletion:
        mock_acompletion.return_value = MockResponse('Mocked async response')
        optimizer = PromptOptimizer()
        test_prompt = "Tell me about Python async"
        result = await optimizer.aoptimize(test_prompt)
        assert isinstance(result, str)
        assert len(result) > 0
        mock_acompletion.assert_called_once()

@pytest.mark.asyncio
async def test_aoptimize_with_custom_config():
    """Test async optimization with custom configuration."""
    with patch('litellm.acompletion', new_callable=AsyncMock) as mock_acompletion:
        mock_acompletion.return_value = MockResponse('Mocked async response')
        custom_optimizer = PromptOptimizer(OptimizationConfig(temperature=0.5))
        test_prompt = "Explain async/await in Python"
        result = await custom_optimizer.aoptimize(test_prompt)
        assert isinstance(result, str)
        assert len(result) > 0
        mock_acompletion.assert_called_once()

@pytest.mark.asyncio
async def test_aoptimize_concurrent():
    """Test concurrent async optimizations."""
    with patch('litellm.acompletion', new_callable=AsyncMock) as mock_acompletion:
        mock_acompletion.return_value = MockResponse('Mocked concurrent response')
        
        optimizer = PromptOptimizer()
        prompts = [
            "What is asyncio?",
            "Explain coroutines",
            "How does async/await work?"
        ]
        
        tasks = [optimizer.aoptimize(prompt) for prompt in prompts]
        results = await asyncio.gather(*tasks)
        
        assert len(results) == len(prompts)
        for result in results:
            assert isinstance(result, str)
            assert len(result) > 0
        assert mock_acompletion.call_count == len(prompts)

@pytest.mark.asyncio
async def test_aoptimize_custom_kwargs():
    """Test async optimization with custom kwargs."""
    with patch('litellm.acompletion', new_callable=AsyncMock) as mock_acompletion:
        mock_acompletion.return_value = MockResponse('Mocked kwargs response')
        optimizer = PromptOptimizer()
        test_prompt = "Explain Python generators"
        result = await optimizer.aoptimize(
            test_prompt,
            temperature=0.8,
            max_tokens=1500
        )
        assert isinstance(result, str)
        assert len(result) > 0
        mock_acompletion.assert_called_once_with(
            messages=[{"role": "user", "content": optimizer.config.template.format(prompt=test_prompt)}],
            model="gpt-4o-mini",
            temperature=0.8,
            max_tokens=1500
        )
