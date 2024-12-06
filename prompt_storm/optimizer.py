"""
Prompt Optimization Module.

This module provides functionality to optimize prompts using LiteLLM.
"""
from typing import Optional
from pydantic import BaseModel, Field
import litellm

class OptimizationConfig(BaseModel):
    """Configuration for prompt optimization."""
    # IMPORTANT: Do not change this model - it must remain gpt-4o-mini for this project
    model: str = Field(default="gpt-4o-mini", description="Model to use for optimization")
    temperature: float = Field(default=0.7, description="Temperature for generation")
    max_tokens: int = Field(default=2000, description="Maximum tokens in response")
    template: str = Field(
        default="As a 10x Prompt Engineer with extensive experience in prompt optimization, "
        "please enhance the following prompt to be more effective, clear, and purposeful:\n\n"
        "{prompt}\n\n"
        "Provide the optimized version only, without any explanations.",
        description="Template for optimization prompt"
    )

class PromptOptimizer:
    """Class for optimizing prompts using LiteLLM."""
    
    def __init__(self, config: Optional[OptimizationConfig] = None):
        """Initialize the prompt optimizer with optional configuration."""
        self.config = config or OptimizationConfig()

    def optimize(self, prompt: str, **kwargs) -> str:
        """
        Optimize the given prompt using LiteLLM.
        
        Args:
            prompt: The prompt to optimize
            **kwargs: Additional arguments to pass to the LiteLLM completion
        
        Returns:
            str: The optimized prompt
        """
        # Prepare the optimization prompt
        optimization_prompt = self.config.template.format(prompt=prompt)
        
        # Merge configuration with any provided kwargs
        completion_kwargs = {
            "model": self.config.model,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            **kwargs
        }
        
        # Get the optimization from LiteLLM
        response = litellm.completion(
            messages=[{"role": "user", "content": optimization_prompt}],
            **completion_kwargs
        )
        
        # Extract and return the optimized prompt
        return response.choices[0].message.content.strip()

    async def aoptimize(self, prompt: str, **kwargs) -> str:
        """
        Asynchronously optimize the given prompt using LiteLLM.
        
        Args:
            prompt: The prompt to optimize
            **kwargs: Additional arguments to pass to the LiteLLM completion
        
        Returns:
            str: The optimized prompt
        """
        # Prepare the optimization prompt
        optimization_prompt = self.config.template.format(prompt=prompt)
        
        # Merge configuration with any provided kwargs
        completion_kwargs = {
            "model": self.config.model,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            **kwargs
        }
        
        # Get the optimization from LiteLLM asynchronously
        response = await litellm.acompletion(
            messages=[{"role": "user", "content": optimization_prompt}],
            **completion_kwargs
        )
        
        # Extract and return the optimized prompt
        return response.choices[0].message.content.strip()

    def optimize_async(self, prompt: str, **kwargs) -> str:
        """
        Deprecated: Use aoptimize instead.
        This method exists for backward compatibility.
        """
        import warnings
        warnings.warn(
            "optimize_async is deprecated and will be removed in a future version. "
            "Use aoptimize instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.optimize(prompt, **kwargs)
