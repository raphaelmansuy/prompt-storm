"""
Service for YAML formatting using LiteLLM.
"""

import litellm
import yaml
from typing import Optional, Dict, Any, List, Union
from prompt_storm.interfaces.service_interfaces import (
    YAMLServiceInterface,
)
from prompt_storm.models.config import YAMLConfig, OptimizationConfig, YAML_EXAMPLE
from prompt_storm.utils.response_processor import (
    extract_content_from_completion,
    strip_markdown,
)


class YAMLService(YAMLServiceInterface):
    """Service for YAML formatting."""

    def __init__(
        self,
        config: Optional[OptimizationConfig] = None
    ):
        """Initialize the YAML service."""
        self.optimization_config = config or OptimizationConfig()
        self.translated_yaml_example = (
            self._translate_yaml_example(YAML_EXAMPLE)
            if self.optimization_config.language != "english"
            else YAML_EXAMPLE
        )
        self.yaml_config = YAMLConfig()

    def _translate_yaml_example(self, yaml_example: str) -> str:
        prompt_translate = f"""
Create the same YAML file with values translated to {self.optimization_config.language}.
Format as markdown, only the YAML code block is needed.
{yaml_example}
        """
        response = litellm.completion(
            model=self.optimization_config.model,
            messages=[{"role": "user", "content": prompt_translate}],
            temperature=self.optimization_config.temperature,
            max_tokens=self.optimization_config.max_tokens,
        )
        result = extract_content_from_completion(response)
        return result

    def _prepare_completion_kwargs(self, **kwargs) -> Dict[str, Any]:
        """Prepare kwargs for completion API call."""
        return {
            "model": self.optimization_config.model,
            "temperature": self.optimization_config.temperature,
            "max_tokens": self.optimization_config.max_tokens,
            **kwargs,
        }

    def _prepare_messages(self, prompt: str) -> list:
        """Prepare messages for completion API call."""
        # Use language from optimization config, default to 'english' if not set
        language = self.optimization_config.language
        yaml_prompt = str(self.yaml_config.template).format(
            prompt=prompt, language=language, yaml_example=self.translated_yaml_example
        )
        system_prompt = "".join(
            [
                "You are prompt_storm (author) and you are an expert at converting prompts into well-structured YAML format.",
                "You will be given a prompt and your task is to convert it into a valid YAML format.",
                "The YAML format should be well-structured and contain all the necessary information to be used effectively.",
                f"Use language: {language} for prompt content, and the description will be in {language}.",
            ]
        )
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": yaml_prompt},
        ]

    def verify_yaml(self, yaml_content: str) -> Union[None, List[str]]:
        """
        Verify if the YAML content is valid.

        Args:
            yaml_content: The YAML content to verify

        Returns:
            None if valid, List of error messages if invalid
        """
        try:
            yaml.safe_load(yaml_content)
            return None
        except yaml.YAMLError as e:
            if hasattr(e, "problem_mark"):
                line = e.problem_mark.line + 1
                column = e.problem_mark.column + 1
                problem = e.problem if hasattr(e, "problem") else "Unknown error"
                return [f"YAML Error at line {line}, column {column}: {problem}"]
            return ["Invalid YAML format: " + str(e)]

    def fix_yaml(self, yaml_content: str) -> str:
        """
        Fix invalid YAML content using LiteLLM.

        Args:
            yaml_content: The YAML content to fix

        Returns:
            str: The fixed YAML content
        """
        try:
            # First verify if it needs fixing
            validation_result = self.verify_yaml(yaml_content)
            if validation_result is None:
                return yaml_content

            # Prepare the fix prompt
            fix_prompt = (
                "Fix the following invalid YAML content. Return only the fixed YAML, no explanations:\n\n"
                f"```yaml\n{yaml_content}\n```\n\n"
                "Errors found:\n" + "\n".join(validation_result)
            )

            completion_kwargs = self._prepare_completion_kwargs()
            messages = [
                {
                    "role": "system",
                    "content": "You are an expert at fixing YAML syntax issues.",
                },
                {"role": "user", "content": fix_prompt},
            ]

            response = litellm.completion(messages=messages, **completion_kwargs)

            fixed_content = extract_content_from_completion(response)
            fixed_content = strip_markdown(fixed_content)

            # Verify the fixed content
            if self.verify_yaml(fixed_content) is not None:
                raise ValueError("Failed to fix YAML content")

            return fixed_content
        except Exception as e:
            raise self.handle_completion_error(e)

    def format_to_yaml(self, prompt: str, **kwargs) -> str:
        """
        Format the given prompt to YAML.

        Args:
            prompt: The prompt to format
            **kwargs: Additional arguments to pass to the LiteLLM completion

        Returns:
            str: The formatted YAML string
        """
        try:
            completion_kwargs = self._prepare_completion_kwargs(**kwargs)
            messages = self._prepare_messages(prompt)

            response = litellm.completion(messages=messages, **completion_kwargs)

            content = extract_content_from_completion(response)
            yaml_content = strip_markdown(content)

            # Verify and fix if needed
            validation_result = self.verify_yaml(yaml_content)
            if validation_result is not None:
                yaml_content = self.fix_yaml(yaml_content)

            return yaml_content
        except Exception as e:
            raise self.handle_completion_error(e)

    def handle_completion_error(self, e: Exception) -> Exception:
        """
        Handle completion errors during YAML formatting.
        
        Args:
            e (Exception): The original exception raised during processing.
        
        Returns:
            Exception: A new exception with a more informative error message.
        """
        error_message = f"Error during YAML completion: {str(e)}"
        return ValueError(error_message)
