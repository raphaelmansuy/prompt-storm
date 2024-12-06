"""
Prompt Optimization Module.

This module provides functionality to optimize prompts using LiteLLM.
"""
from typing import Optional
from pydantic import BaseModel, Field
import litellm

class OptimizationConfig(BaseModel):
    """Configuration for prompt optimization."""
    model: str = Field(default="gpt-4o-mini", description="Model to use for optimization")
    temperature: float = Field(default=0.7, description="Temperature for generation")
    max_tokens: int = Field(default=2000, description="Maximum tokens in response")
    template: str = Field(
        default=(
            "As an expert Prompt Engineer, enhance the following prompt:\n\n"
            "```\n{prompt}\n```\n\n"
            "Optimization Guidelines:\n"
            "1. Improve clarity, conciseness, and effectiveness\n"
            "2. Use variables (e.g., {{{{variable_name}}}}) for customization, variable in snake_case\n"
            "3. Apply appropriate formatting for better structure\n"
            "4. Add context or specific instructions where needed\n"
            "5. Ensure the prompt elicits precise, relevant responses\n"
            "6. Address potential biases and ethical concerns\n"
            "7. Tailor for the intended model and use case\n"
            "8. Consider edge cases and possible misinterpretations\n"
            "9. Balance human readability with AI comprehension\n"
            "10. Incorporate a suitable persona if beneficial\n"
            "11. Use clear, unambiguous language\n"
            "12. Include examples or demonstrations if helpful\n"
            "13. Induce CoT, Chain of Thought if applicable\n\n"
            "Provide only the optimized prompt. No explanations or comments."
        ),
        description="Template for prompt optimization"
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
        
        # Get completion from LiteLLM
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
        
        # Get completion from LiteLLM asynchronously
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
