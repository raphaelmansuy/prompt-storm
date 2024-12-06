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
    
    # Template for YAML formatting
    YAML_FORMAT_TEMPLATE = (
        "You are prompt_storm (author) and you are an expert at converting prompts into well-structured YAML format. Convert the following prompt into a well-structured YAML format following this structure:\n"
        "- Include metadata (name, version, description, author)\n"
        "- Extract input variables with type, description, and examples\n"
        "- Add relevant tags and categories\n"
        "- Include the original content\n\n"
        "Prompt to convert:\n```\n{prompt}\n```\n\n"
        "Return only valid YAML. Follow this example structure:\n"
        "```yaml\n"
        "name: prompt_name\n"
        "version: '1.0'\n"
        "description: >-\n"
        "  A clear description of the prompt's purpose\n"
        "author: author_name\n"
        "input_variables:\n"
        "  variable_name:\n"
        "    type: string\n"
        "    description: Description of the variable\n"
        "    examples:\n"
        "      - 'Example 1'\n"
        "      - 'Example 2'\n"
        "tags:\n"
        "  - relevant_tag1\n"
        "  - relevant_tag2\n"
        "categories:\n"
        "  - category1\n"
        "content: >-\n"
        "  Original prompt content\n"
        "```"
    )

    # System message for YAML formatting
    YAML_FORMAT_SYSTEM_MESSAGE = {
        "role": "system",
        "content": "You are an expert at converting prompts into well-structured YAML format."
    }
    
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

    def _process_yaml_content(self, completion) -> str:
        """
        Process the YAML content from the completion response.
        
        Args:
            completion: The completion response containing the YAML content
            
        Returns:
            str: The processed YAML content with markdown markers removed
            
        Raises:
            RuntimeError: If the model encounters a rate limit error
        """
        try:
            content = completion.choices[0].message.content.strip()
            
            # Remove markdown code block markers if present
            import re
            content = re.sub(r'^```ya?ml\s*\n', '', content, flags=re.MULTILINE)
            content = re.sub(r'\n```\s*$', '', content, flags=re.MULTILINE)
            
            return content.strip()
            
        except Exception as e:
            # Debug print statement
            print(f"Exception encountered: {e}")
            # Check if the error message indicates a rate limit issue
            if "rate limit exceeded" in str(e).lower() or "resource_exhausted" in str(e).lower():
                raise RuntimeError("Rate limit exceeded for model. Please try again in about an hour.") from e
            raise

    def format_to_yaml(self, prompt: str, **kwargs) -> str:
        """
        Format the given prompt into a YAML string using LiteLLM.
        
        Args:
            prompt: The prompt to format
            **kwargs: Additional arguments to pass to the LiteLLM completion
            
        Returns:
            str: The formatted YAML string with any markdown code block markers removed
            
        Raises:
            RuntimeError: If the model encounters a rate limit error
        """
        messages = [
            self.YAML_FORMAT_SYSTEM_MESSAGE,
            {
                "role": "user",
                "content": self.YAML_FORMAT_TEMPLATE.format(prompt=prompt)
            }
        ]
        
        completion = litellm.completion(
            model=self.config.model,
            messages=messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            **kwargs
        )
        
        return self._process_yaml_content(completion)

    async def aformat_to_yaml(self, prompt: str, **kwargs) -> str:
        """
        Asynchronously format the given prompt into a YAML string using LiteLLM.
        
        Args:
            prompt: The prompt to format
            **kwargs: Additional arguments to pass to the LiteLLM completion
            
        Returns:
            str: The formatted YAML string with any markdown code block markers removed
            
        Raises:
            RuntimeError: If the model encounters a rate limit error
        """
        messages = [
            self.YAML_FORMAT_SYSTEM_MESSAGE,
            {
                "role": "user",
                "content": self.YAML_FORMAT_TEMPLATE.format(prompt=prompt)
            }
        ]
        
        completion = await litellm.acompletion(
            model=self.config.model,
            messages=messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            **kwargs
        )
        
        return self._process_yaml_content(completion)
