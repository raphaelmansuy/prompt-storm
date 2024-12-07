"""
Configuration models for the prompt_storm package.
"""

from pydantic import BaseModel, Field

YAML_EXAMPLE = """
```yaml
name: "prompt_name"
version: '1.0'
description: >-
  A clear description of the prompt's purpose
author: quantalogic
input_variables:
  variable_name:
    type: string
    description: >-
      A description of the variable
    examples:
      - "Example 1"
      - "Example 2"
tags:
  - "relevant_tag1"
  - "relevant_tag2"
categories:
  - "category1"
content: >-
  Original prompt content
```
"""

class OptimizationConfig(BaseModel):
    """Configuration for prompt optimization."""

    model: str = Field(
        default="gpt-4o-mini", description="Model to use for optimization"
    )
    temperature: float = Field(default=0.7, description="Temperature for generation")
    max_tokens: int = Field(default=2000, description="Maximum tokens in response")
    language: str = Field(default="english", description="Language for optimization")
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
            "13. Induce CoT, Chain of Thought if applicable, to reason step by step\n\n"
            "Provide only the optimized prompt. No explanations or comments."
        ),
        description="Template for prompt optimization",
    )


class YAMLConfig(BaseModel):
    """Configuration for YAML formatting."""
    template: str = Field(
        default=(
            "You are prompt_storm (author) and you are an expert at converting prompts into "
            "well-structured YAML format. Convert the following prompt into a well-structured "
            "YAML format following this structure:\n"
            "- Include metadata (name, version, description, author) in {language}\n"
            "- Extract input variables with type, description, and examples in {language}\n"
            "- Add relevant tags and categories\n"
            "- Include the original content in {language}\n\n"
            "Prompt to convert:\n```\n{prompt}\n```\n\n"
            "Very important: name, description, tags, categories, and content MUST all be in {language}.\n"
            "Return only valid YAML. Follow this example structure:\n",
            "{yaml_example}\n\n",
        ),
        description="Template for YAML formatting",
    )
