"""
Prompt Optimization Module.

This module provides functionality to optimize prompts using LiteLLM.
"""
from typing import Optional, List, Union, Dict
from pydantic import BaseModel, Field
import litellm
import yaml
from dataclasses import dataclass

@dataclass
class YAMLValidationError:
    """Represents a YAML validation error."""
    message: str
    line: Optional[int] = None
    column: Optional[int] = None

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
            error_msg = str(e).lower()
            if "rate limit" in error_msg or "resource_exhausted" in error_msg:
                raise RuntimeError(
                    "Rate limit exceeded for model. Please wait a few minutes and try again, "
                    "or consider upgrading your API plan for higher rate limits."
                ) from e
            raise RuntimeError(f"Error processing YAML content: {str(e)}") from e

    def _prepare_messages(self, prompt: str) -> List[dict]:
        """
        Prepare messages for both sync and async versions.
        
        Args:
            prompt: The prompt to format
            
        Returns:
            List[dict]: List of messages for the LLM
        """
        return [
            self.YAML_FORMAT_SYSTEM_MESSAGE,
            {
                "role": "user",
                "content": self.YAML_FORMAT_TEMPLATE.format(prompt=prompt)
            }
        ]

    def _prepare_completion_kwargs(self, **kwargs) -> dict:
        """
        Prepare completion kwargs for both versions.
        
        Args:
            **kwargs: Additional arguments to pass to the LiteLLM completion
            
        Returns:
            dict: Combined completion arguments
        """
        return {
            "model": self.config.model,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            **kwargs
        }

    def _handle_yaml_errors(self, errors: Optional[List[YAMLValidationError]]) -> None:
        """
        Handle YAML validation errors for both versions.
        
        Args:
            errors: List of YAML validation errors if any
            
        Raises:
            ValueError: If there are any YAML validation errors
        """
        if errors:
            error_messages = []
            for e in errors:
                if e.line and e.column:
                    error_messages.append(f"Line {e.line}, Column {e.column}: {e.message}")
                else:
                    error_messages.append(e.message)
            
            error_str = "\n".join(error_messages)
            raise ValueError(
                f"Generated YAML is invalid. Please ensure all required fields "
                f"(name, version, description, content) are present and properly formatted:\n{error_str}"
            )

    def _base_format_to_yaml(self, completion) -> str:
        """
        Base method for processing YAML formatting results.
        
        Args:
            completion: The completion response from LiteLLM
            
        Returns:
            str: Processed and validated YAML content
            
        Raises:
            ValueError: If the generated YAML is invalid
        """
        yaml_content = self._process_yaml_content(completion)
        errors = self.verify_yaml(yaml_content)
        self._handle_yaml_errors(errors)
        return yaml_content

    def format_to_yaml(self, prompt: str, **kwargs) -> str:
        """
        Format a prompt into a YAML format.

        Args:
            prompt: The prompt to format
            **kwargs: Additional keyword arguments to pass to the completion API

        Returns:
            str: The formatted YAML content

        Raises:
            RuntimeError: If there is an error during formatting
        """
        try:
            completion = litellm.completion(
                model=self.config.model,
                messages=[{
                    "role": "user",
                    "content": self.YAML_FORMAT_TEMPLATE.format(prompt=prompt)
                }],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                **kwargs
            )
            
            return self._base_format_to_yaml(completion)
        except Exception as e:
            error_msg = str(e)
            if "rate limit" in error_msg.lower():
                raise RuntimeError(
                    "Rate limit exceeded for model. Please wait a few minutes before trying again."
                ) from e
            raise RuntimeError(f"Error formatting prompt to YAML: {error_msg}") from e

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
            ValueError: If the generated YAML is invalid
        """
        messages = self._prepare_messages(prompt)
        completion_kwargs = self._prepare_completion_kwargs(**kwargs)
        
        completion = await litellm.acompletion(
            messages=messages,
            **completion_kwargs
        )
        
        yaml_content = self._base_format_to_yaml(completion)
        
        # Verify and attempt to fix if invalid
        errors = self.verify_yaml(yaml_content)
        if errors:
            try:
                yaml_content = await self.fix_yaml(yaml_content)
                errors = self.verify_yaml(yaml_content)
                self._handle_yaml_errors(errors)
            except Exception as e:
                raise ValueError(f"Failed to fix YAML: {str(e)}")
        
        return yaml_content

    def verify_yaml(self, yaml_content: str) -> Union[None, List[YAMLValidationError]]:
        """
        Verify if the YAML content is valid.
        
        Args:
            yaml_content: The YAML content to verify
            
        Returns:
            None if valid, List[YAMLValidationError] if invalid
        """
        try:
            # Try to parse the YAML content
            data = yaml.safe_load(yaml_content)
            
            # Basic validation
            if not isinstance(data, dict):
                return [YAMLValidationError(message="YAML content must be a dictionary")]
                
            # Required fields validation
            required_fields = ['name', 'version', 'description', 'content']
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                return [YAMLValidationError(
                    message=f"Missing required fields: {', '.join(missing_fields)}"
                )]
                
            return None
        except yaml.YAMLError as e:
            # Convert YAML error to our custom error format
            if hasattr(e, 'problem_mark'):
                return [YAMLValidationError(
                    message=str(e.problem),
                    line=e.problem_mark.line + 1,
                    column=e.problem_mark.column + 1
                )]
            return [YAMLValidationError(message=str(e))]

    async def fix_yaml(self, yaml_content: str) -> str:
        """
        Fix invalid YAML content using LiteLLM.
        
        Args:
            yaml_content: The invalid YAML content to fix
            
        Returns:
            str: The fixed YAML content
            
        Raises:
            RuntimeError: If the model encounters a rate limit error
        """
        fix_template = (
            "Fix the following invalid YAML content. Ensure it follows the correct structure "
            "with required fields (name, version, description, content). "
            "Return only the fixed YAML, no explanations.\n\n"
            "Invalid YAML:\n```yaml\n{yaml_content}\n```"
        )
        
        messages = [
            {
                "role": "system",
                "content": "You are an expert at fixing YAML syntax and structure issues."
            },
            {
                "role": "user",
                "content": fix_template.format(yaml_content=yaml_content)
            }
        ]
        
        completion = await litellm.acompletion(
            model=self.config.model,
            messages=messages,
            temperature=0.2,  # Lower temperature for more consistent fixes
            max_tokens=self.config.max_tokens
        )
        
        return self._process_yaml_content(completion)
