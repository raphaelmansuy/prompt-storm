# Table of Contents
- prompt_storm/prompt_format.py
- prompt_storm/__init__.py
- prompt_storm/cli.py
- prompt_storm/optimizer.py
- prompt_storm/utils/logger.py
- prompt_storm/utils/response_processor.py
- prompt_storm/utils/error_handler.py
- prompt_storm/models/responses.py
- prompt_storm/models/config.py
- prompt_storm/services/csv_service.py
- prompt_storm/services/optimizer_service.py
- prompt_storm/services/yaml_service.py
- prompt_storm/services/batch_optimizer_service.py
- prompt_storm/interfaces/service_interfaces.py
- pyproject.toml
- tests/test_optimizer.py
- tests/conftest.py
- tests/test_placeholder.py
- tests/test_cli.py

## File: prompt_storm/prompt_format.py

- Extension: .py
- Language: python
- Size: 1214 bytes
- Created: 2024-12-06 13:16:30
- Modified: 2024-12-06 13:16:30

### Code

```python


PROMPT_FORMAT_EXAMPLE = """
name: illustration_pattern
version: "1.0"
description: >
    This prompt is designed to help creative artists to illustrate the concept of a subject through a unique and engaging pattern.
author: quantalogic
input_variables:
  subject:
    type: string
    description: The subject to illustrate
    place_holder: "Marketing"
    examples: 
      - "Marketing"
      - "Design"
      - "Art"
  emotion:
    type: string
    description: Emotion to convey
    place_holder: "Excitement"
    examples: 
      - "Excitement"
      - "Confidence"
      - "Hope"
  inspiration: 
    type: string
    description: Sources of inspiration
    place_holder: "Architecture"
    examples: 
      - "Architecture"
      - "Art"
      - "Design"
  palette:
    type: string
    description: The color palette to use
    place_holder: "Pastel"
    examples: 
      - "Pastel"
      - "Vibrant"
      - "Monochrome"
tags: 
  - creative
  - illustration
categories:
  - art

content: >

  As a creative artist, I am tasked with illustrating the concept of a subject through a unique and engaging pattern.

  - First I will choose a primary color palette that reflects the essence of the subject. 
"""
```

## File: prompt_storm/__init__.py

- Extension: .py
- Language: python
- Size: 163 bytes
- Created: 2024-12-06 11:01:28
- Modified: 2024-12-06 11:01:28

### Code

```python
"""
Prompt Storm: Advanced Prompt Engineering Toolkit

This package provides tools for sophisticated prompt generation and engineering.
"""

__version__ = "0.1.0"

```

## File: prompt_storm/cli.py

- Extension: .py
- Language: python
- Size: 9877 bytes
- Created: 2024-12-08 10:34:16
- Modified: 2024-12-08 10:34:16

### Code

```python
"""
Command Line Interface for Prompt Storm.

This module provides the CLI functionality for the prompt-storm package.
"""
import sys
from typing import Optional
import click
from rich.console import Console
from .optimizer import PromptOptimizer, OptimizationConfig
from .services.yaml_service import YAMLService
from .services.csv_service import CSVService
from .services.batch_optimizer_service import BatchOptimizerService
from .utils.logger import setup_logger, console

# Initialize with non-verbose logging by default
logger = setup_logger(__name__, verbose=False)

@click.group()
def cli():
    """Prompt Storm CLI - A tool for prompt engineering and optimization."""
    pass

@cli.command()
@click.argument('prompt', type=str)
@click.option('--model', '-m', 
              help='Model to use for optimization',
              default="gpt-4o-mini")
@click.option('--max-tokens', '-t',
              help='Maximum tokens in response',
              type=click.IntRange(min=1),
              default=2000)
@click.option('--temperature', '-temp',
              help='Temperature for generation',
              type=click.FloatRange(min=0.0, max=1.0),
              default=0.7)
@click.option('--input-file', '-i',
              help='Input file containing the prompt',
              type=click.Path(exists=True, dir_okay=False),
              default=None)
@click.option('--output-file', '-o',
              help='Output file to save the optimized prompt',
              type=click.Path(dir_okay=False),
              default=None)
@click.option('--yaml', '-y',
              help='Format the optimized prompt as YAML',
              is_flag=True,
              default=False)
@click.option('--verbose', '-v',
              help='Enable verbose logging',
              is_flag=True,
              default=False)
def optimize(prompt: str,
            model: str,
            max_tokens: int,
            temperature: float,
            input_file: Optional[str],
            output_file: Optional[str],
            yaml: bool,
            verbose: bool):
    """
    Optimize a prompt using LLM.
    
    If --input-file is provided, the prompt argument is ignored and the content
    of the file is used instead.

    If --yaml flag is set, the optimized prompt will be formatted as YAML.
    """
    try:
        # Set up logger with verbose setting
        global logger
        logger = setup_logger(__name__, verbose=verbose)
        
        if verbose:
            logger.debug("Verbose logging enabled")
            logger.info(f"Prompt: {prompt}")
            logger.info(f"Model: {model}")
        
        # Read from input file if provided
        if input_file:
            with open(input_file, 'r', encoding='utf-8') as f:
                prompt = f.read().strip()

        # Create configuration
        config = OptimizationConfig(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        
        # Initialize optimizer and optimize prompt
        optimizer = PromptOptimizer(config)
        optimized_prompt = optimizer.optimize(prompt)
        
        # Format as YAML if requested
        if yaml:
            optimized_prompt = optimizer.format_to_yaml(optimized_prompt)
        
        # Handle output
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(optimized_prompt)
            logger.info(f"Optimized prompt saved to {output_file}")
        else:
            console.print(optimized_prompt)
            
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=verbose)
        sys.exit(1)

@cli.command()
@click.argument('input-csv', type=click.Path(exists=True, dir_okay=False))
@click.argument('output-dir', type=click.Path(file_okay=False))
@click.option('--prompt-column', '-c',
              help='Name of the column containing prompts',
              default='prompt')
@click.option('--model', '-m', 
              help='Model to use for optimization',
              default="gpt-4o-mini")
@click.option('--max-tokens', '-t',
              help='Maximum tokens in response',
              type=click.IntRange(min=1),
              default=2000)
@click.option('--temperature', '-temp',
              help='Temperature for generation',
              type=click.FloatRange(min=0.0, max=1.0),
              default=0.7)
@click.option('--language', '-l',
              help='Language for optimization',
              default="english")
@click.option('--verbose', '-v',
              help='Enable verbose logging',
              is_flag=True,
              default=False)
def optimize_batch(input_csv: str,
                  output_dir: str,
                  prompt_column: str,
                  model: str,
                  max_tokens: int,
                  temperature: float,
                  language: str,
                  verbose: bool):
    """
    Optimize a batch of prompts from a CSV file.
    
    The optimized prompts will be saved as YAML files in categorized subdirectories.
    Each prompt will be analyzed to determine its category and an appropriate name.
    """
    try:
        # Set up logger with verbose setting
        global logger
        logger = setup_logger(__name__, verbose=verbose)
        
        if verbose:
            logger.debug("Verbose logging enabled")
            logger.info(f"Input CSV: {input_csv}")
            logger.info(f"Output directory: {output_dir}")
            logger.info(f"Model: {model}")
            logger.info(f"Language: {language}")

        # Create configuration
        config = OptimizationConfig(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            language=language
        )

        # Initialize services
        optimizer_service = PromptOptimizer(config)
        yaml_service = YAMLService(config)
        csv_service = CSVService()
        
        # Initialize batch optimizer with services
        batch_optimizer = BatchOptimizerService(
            optimizer_service=optimizer_service,
            yaml_service=yaml_service,
            csv_service=csv_service,
            verbose=verbose
        )
        
        # Run batch optimization
        results = batch_optimizer.optimize_batch(
            input_csv=input_csv,
            output_dir=output_dir,
            prompt_column=prompt_column,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            language=language
        )
        
        # Print final summary
        success_count = sum(1 for r in results.values() if not r.startswith("ERROR:"))
        console.print("\n[bold green]Batch Processing Complete[/bold green]")
        console.print(f"Successfully processed: [green]{success_count}[/green] out of [blue]{len(results)}[/blue] prompts")
        
        if success_count < len(results):
            console.print("\n[yellow]Errors encountered:[/yellow]")
            for prompt, result in results.items():
                if result.startswith("ERROR:"):
                    console.print(f"[red]{result}[/red]")
                    
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=verbose)
        sys.exit(1)

@cli.command()
@click.argument('prompt', type=str)
@click.option('--input-file', '-i', help='Input file containing the prompt', type=click.Path(exists=True, dir_okay=False), default=None)
@click.option('--output-file', '-o', help='Output file to save the formatted YAML', type=click.Path(dir_okay=False), default=None)
@click.option('--verbose', '-v', help='Enable verbose logging', is_flag=True, default=False)
@click.option('--language', '-l', help='Language for optimization', default="english")
@click.option('--model', '-m', help='Model to use for optimization', default="gpt-4o-mini")
@click.option('--max-tokens', '-t', help='Maximum tokens in response', type=click.IntRange(min=1), default=2000)
@click.option('--temperature', '-temp', help='Temperature for generation', type=click.FloatRange(min=0.0, max=1.0), default=0.7)
def format_prompt(prompt: str, input_file: Optional[str], output_file: Optional[str], verbose: bool, language: str, model: str, max_tokens: int, temperature: float):
    """Format a provided prompt into YAML. If --input-file is specified, the content of the file is used instead."""
    try:
        # Set up logger with verbose setting
        global logger
        logger = setup_logger(__name__, verbose=verbose)
        if verbose:
            logger.debug("Verbose logging enabled")
            # display parameters
            logger.info(f"Prompt: {prompt}")
            logger.info(f"Language: {language}")
            logger.info(f"Model: {model}")
            logger.info(f"Max Tokens: {max_tokens}")
            logger.info(f"Temperature: {temperature}")

        # Create configuration
        config = OptimizationConfig(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            language=language
        )

        
        # Load prompt from file if specified
        if input_file:
            with open(input_file, 'r', encoding='utf-8') as f:
                prompt = f.read().strip()
        
        # Initialize YAML service and format
        yaml_service = YAMLService(config)
        formatted_yaml = yaml_service.format_to_yaml(prompt)

        # Handle output
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(formatted_yaml)
            console.print(f"Formatted prompt saved to {output_file}")
        else:
            console.print(formatted_yaml)

    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=verbose)
        sys.exit(1)

if __name__ == '__main__':
    cli()

```

## File: prompt_storm/optimizer.py

- Extension: .py
- Language: python
- Size: 1526 bytes
- Created: 2024-12-07 12:57:51
- Modified: 2024-12-07 12:57:51

### Code

```python
"""
Prompt Optimization Module.

This module provides functionality to optimize prompts using LiteLLM.
"""
from typing import Optional
from prompt_storm.models.config import OptimizationConfig
from prompt_storm.services.optimizer_service import OptimizerService
from prompt_storm.services.yaml_service import YAMLService

class PromptOptimizer:
    """Class for optimizing prompts using LiteLLM."""
    
    def __init__(self, config: Optional[OptimizationConfig] = None):
        """Initialize the prompt optimizer with optional configuration."""
        self.config = config or OptimizationConfig()
        self._optimizer_service = OptimizerService(self.config)
        self._yaml_service = YAMLService(self.config)

    def optimize(self, prompt: str, **kwargs) -> str:
        """
        Optimize the given prompt using LiteLLM.
        
        Args:
            prompt: The prompt to optimize
            **kwargs: Additional arguments to pass to the LiteLLM completion
        
        Returns:
            str: The optimized prompt
        """
        return self._optimizer_service.optimize(prompt, **kwargs)

    def format_to_yaml(self, prompt: str, **kwargs) -> str:
        """
        Format the given prompt to YAML.
        
        Args:
            prompt: The prompt to format
            **kwargs: Additional arguments to pass to the LiteLLM completion
            
        Returns:
            str: The formatted YAML string
        """
        return self._yaml_service.format_to_yaml(prompt, **kwargs)
```

## File: prompt_storm/utils/logger.py

- Extension: .py
- Language: python
- Size: 2481 bytes
- Created: 2024-12-07 11:35:49
- Modified: 2024-12-07 11:35:49

### Code

```python
"""
Logging utility for prompt-storm.
"""
import logging
import sys
from typing import Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskID
from rich.logging import RichHandler

console = Console()
progress = Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    console=console,
)

def setup_logger(name: str, verbose: bool = False) -> logging.Logger:
    """Set up a logger with rich formatting."""
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, show_path=verbose)]
    )
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger

class BatchProgressTracker:
    """Track progress of batch operations with rich output."""
    
    def __init__(self, total: int, description: str = "Processing"):
        """Initialize progress tracker."""
        self.total = total
        self.description = description
        self.task_id: Optional[TaskID] = None
        self.current = 0
        
    def __enter__(self) -> 'BatchProgressTracker':
        """Start progress tracking."""
        progress.start()
        self.task_id = progress.add_task(self.description, total=self.total)
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop progress tracking."""
        progress.stop()
        
    def update(self, advance: int = 1, status: str = ""):
        """Update progress with optional status message."""
        if status:
            progress.update(self.task_id, description=f"{self.description} - {status}")
        progress.advance(self.task_id, advance)
        self.current += advance
        
    def log_success(self, message: str):
        """Log a success message."""
        console.print(f"✅ {message}", style="green")
        
    def log_error(self, message: str):
        """Log an error message."""
        console.print(f"❌ {message}", style="red")
        
    def log_warning(self, message: str):
        """Log a warning message."""
        console.print(f"⚠️  {message}", style="yellow")
        
    def log_info(self, message: str):
        """Log an info message."""
        console.print(f"ℹ️  {message}", style="blue")

```

## File: prompt_storm/utils/response_processor.py

- Extension: .py
- Language: python
- Size: 631 bytes
- Created: 2024-12-07 10:27:27
- Modified: 2024-12-07 10:27:27

### Code

```python
"""
Utility functions for processing responses.
"""
import re
from typing import Any

def strip_markdown(content: str) -> str:
    """Remove markdown code block markers from content."""
    content = content.strip()
    # Remove markdown code block markers with or without language specifier
    content = re.sub(r'^```\w*\s*\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'\n```\s*$', '', content, flags=re.MULTILINE)
    return content.strip()

def extract_content_from_completion(completion: Any) -> str:
    """Extract content from a completion response."""
    return completion.choices[0].message.content.strip()

```

## File: prompt_storm/utils/error_handler.py

- Extension: .py
- Language: python
- Size: 627 bytes
- Created: 2024-12-07 13:12:13
- Modified: 2024-12-07 13:12:13

### Code

```python
"""
Error handling utilities.
"""
from typing import Optional, Union
from prompt_storm.models.responses import YAMLValidationError

def handle_completion_error(error: Exception) -> None:
    """Handle errors from completion API calls."""
    error_msg = str(error).lower()
    if "rate limit" in error_msg or "resource_exhausted" in error_msg:
        raise RuntimeError(
            "Rate limit exceeded for model. Please wait a few minutes and try again, "
            "or consider upgrading your API plan for higher rate limits."
        )
    raise YAMLValidationError(message=f"Error processing completion: {str(error)}")

```

## File: prompt_storm/models/responses.py

- Extension: .py
- Language: python
- Size: 1066 bytes
- Created: 2024-12-07 13:25:34
- Modified: 2024-12-07 13:25:34

### Code

```python
"""
Response models for the prompt_storm package.
"""
from typing import Optional

class YAMLValidationError(Exception):
    """Represents a YAML validation error."""
    def __init__(self, message: str, line: Optional[int] = None, column: Optional[int] = None):
        """
        Initialize the YAML validation error.
        
        Args:
            message: Error message describing the validation issue
            line: Optional line number where the error occurred
            column: Optional column number where the error occurred
        """
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column

    def __str__(self):
        """
        Provide a string representation of the error.
        
        Returns:
            A formatted error message including line and column if available
        """
        base_msg = self.message
        if self.line is not None and self.column is not None:
            base_msg += f" (line {self.line}, column {self.column})"
        return base_msg

```

## File: prompt_storm/models/config.py

- Extension: .py
- Language: python
- Size: 3243 bytes
- Created: 2024-12-07 22:13:22
- Modified: 2024-12-07 22:13:22

### Code

```python
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

```

## File: prompt_storm/services/csv_service.py

- Extension: .py
- Language: python
- Size: 1152 bytes
- Created: 2024-12-07 12:54:20
- Modified: 2024-12-07 12:54:20

### Code

```python
"""
Service for CSV processing.
"""
import pandas as pd
from typing import List
from prompt_storm.interfaces.service_interfaces import CSVServiceInterface

class CSVService(CSVServiceInterface):
    """Service for reading prompts from CSV files."""
    
    def read_prompts(self, csv_path: str, prompt_column: str) -> List[str]:
        """
        Read prompts from a CSV file.
        
        Args:
            csv_path: Path to the CSV file
            prompt_column: Name of the column containing prompts
            
        Returns:
            List of prompts
            
        Raises:
            FileNotFoundError: If CSV file doesn't exist
            KeyError: If prompt column doesn't exist
        """
        try:
            df = pd.read_csv(csv_path)
            if prompt_column not in df.columns:
                raise KeyError(f"Column '{prompt_column}' not found in CSV file")
            return df[prompt_column].tolist()
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found at: {csv_path}")
        except Exception as e:
            raise Exception(f"Error reading CSV file: {str(e)}")

```

## File: prompt_storm/services/optimizer_service.py

- Extension: .py
- Language: python
- Size: 2059 bytes
- Created: 2024-12-07 12:53:36
- Modified: 2024-12-07 12:53:36

### Code

```python
"""
Service for optimizing prompts using LiteLLM.
"""
import litellm
from typing import Optional, Dict, Any
from prompt_storm.interfaces.service_interfaces import OptimizerServiceInterface
from prompt_storm.models.config import OptimizationConfig
from prompt_storm.utils.response_processor import extract_content_from_completion, strip_markdown
from prompt_storm.utils.error_handler import handle_completion_error

class OptimizerService(OptimizerServiceInterface):
    """Service for optimizing prompts."""
    
    def __init__(self, config: Optional[OptimizationConfig] = None):
        """Initialize the optimizer service."""
        self.config = config or OptimizationConfig()
    
    def _prepare_completion_kwargs(self, **kwargs) -> Dict[str, Any]:
        """Prepare kwargs for completion API call."""
        return {
            "model": self.config.model,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            **kwargs
        }
    
    def _prepare_messages(self, prompt: str) -> list:
        """Prepare messages for completion API call."""
        optimization_prompt = self.config.template.format(prompt=prompt)
        return [{"role": "user", "content": optimization_prompt}]
    
    def optimize(self, prompt: str, **kwargs) -> str:
        """
        Optimize the given prompt.
        
        Args:
            prompt: The prompt to optimize
            **kwargs: Additional arguments to pass to the LiteLLM completion
        
        Returns:
            str: The optimized prompt
        """
        try:
            completion_kwargs = self._prepare_completion_kwargs(**kwargs)
            messages = self._prepare_messages(prompt)
            
            response = litellm.completion(
                messages=messages,
                **completion_kwargs
            )
            
            content = extract_content_from_completion(response)
            return strip_markdown(content)
        except Exception as e:
            raise handle_completion_error(e)

```

## File: prompt_storm/services/yaml_service.py

- Extension: .py
- Language: python
- Size: 6769 bytes
- Created: 2024-12-08 10:35:16
- Modified: 2024-12-08 10:35:16

### Code

```python
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

```

## File: prompt_storm/services/batch_optimizer_service.py

- Extension: .py
- Language: python
- Size: 6866 bytes
- Created: 2024-12-07 13:35:44
- Modified: 2024-12-07 13:35:44

### Code

```python
"""
Service for batch optimization of prompts.
"""
from pathlib import Path
from typing import Dict, Optional
import yaml
from prompt_storm.interfaces.service_interfaces import (
    BatchOptimizerServiceInterface,
    OptimizerServiceInterface,
    YAMLServiceInterface,
    CSVServiceInterface
)
from prompt_storm.models.config import OptimizationConfig
from prompt_storm.utils.logger import BatchProgressTracker, setup_logger

logger = setup_logger(__name__, verbose=False)

class BatchOptimizerService(BatchOptimizerServiceInterface):
    """Service for batch optimization of prompts."""
    
    def __init__(
        self,
        optimizer_service: OptimizerServiceInterface,
        yaml_service: YAMLServiceInterface,
        csv_service: CSVServiceInterface,
        config: Optional[OptimizationConfig] = None,
        verbose: bool = False
    ):
        """Initialize the batch optimizer service."""
        self.optimizer_service = optimizer_service
        self.yaml_service = yaml_service
        self.csv_service = csv_service
        self.config = config or OptimizationConfig()
        self.verbose = verbose
        global logger
        logger = setup_logger(__name__, verbose=verbose)
        
    def _infer_category_and_name(self, prompt: str) -> tuple[str, str]:
        """
        Infer category and name from YAML inference.
        
        Args:
            prompt: The prompt to categorize
            
        Returns:
            Tuple of (category, name)
        """
        try:
            # Get YAML representation
            yaml_content = self.yaml_service.format_to_yaml(prompt)
            
            # Parse YAML to get category and name
            yaml_data = yaml.safe_load(yaml_content)
            
            # Extract first category and name
            category = yaml_data.get('categories', ['general'])[0].lower()
            name = yaml_data.get('name', 'unnamed-prompt').lower()
            
            if self.verbose:
                logger.debug(f"Inferred from YAML - category: {category}, name: {name}")
            
            return category, name
            
        except Exception as e:
            logger.warning(f"Error inferring from YAML: {str(e)}")
            return "general", "unnamed-prompt"
        
    def _get_unique_filepath(self, directory: Path, filename: str) -> Path:
        """Get a unique filepath by appending numbers if necessary."""
        base = directory / filename
        if not base.exists():
            return base
            
        counter = 1
        while True:
            new_path = directory / f"{filename.rsplit('.', 1)[0]}_{counter}.yaml"
            if not new_path.exists():
                if self.verbose:
                    logger.debug(f"Generated unique filepath: {new_path}")
                return new_path
            counter += 1
            
    def optimize_batch(
        self,
        input_csv: str,
        output_dir: str,
        prompt_column: str,
        model: str = None,
        max_tokens: int = None,
        temperature: float = None,
        language: str = None
    ) -> Dict[str, str]:
        """
        Optimize a batch of prompts from CSV and save to YAML files.
        
        Args:
            input_csv: Path to input CSV file
            output_dir: Directory to save optimized prompts
            prompt_column: Name of the column containing prompts
            model: Model to use for optimization (optional)
            max_tokens: Maximum tokens in response (optional)
            temperature: Temperature for generation (optional)
            language: Language for optimization (optional)
            
        Returns:
            Dictionary mapping original prompts to output file paths
        """
        # Update config with any provided parameters
        if model is not None:
            self.config.model = model
        if max_tokens is not None:
            self.config.max_tokens = max_tokens
        if temperature is not None:
            self.config.temperature = temperature
        if language is not None:
            self.config.language = language

        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        if self.verbose:
            logger.info(f"Created output directory: {output_dir}")
        
        # Read prompts
        if self.verbose:
            logger.info(f"Reading prompts from {input_csv}")
        prompts = self.csv_service.read_prompts(input_csv, prompt_column)
        if self.verbose:
            logger.info(f"Found {len(prompts)} prompts to process")
        
        # Process each prompt
        results = {}
        with BatchProgressTracker(len(prompts), "Optimizing prompts") as progress:
            for i, prompt in enumerate(prompts, 1):
                try:
                    # Update progress with current prompt number
                    progress.update(status=f"Prompt {i}/{len(prompts)}")
                    
                    # Optimize prompt
                    if self.verbose:
                        logger.debug(f"Optimizing prompt {i}")
                    optimized = self.optimizer_service.optimize(prompt)
                    
                    # Infer category and name
                    if self.verbose:
                        logger.debug(f"Categorizing prompt {i}")
                    category, name = self._infer_category_and_name(prompt)
                    
                    # Create category directory
                    category_dir = output_path / category
                    category_dir.mkdir(exist_ok=True)
                    
                    # Get unique filepath
                    filepath = self._get_unique_filepath(category_dir, f"{name}.yaml")
                    
                    # Format and save as YAML
                    if self.verbose:
                        logger.debug(f"Saving prompt {i} to {filepath}")
                    yaml_content = self.yaml_service.format_to_yaml(optimized)
                    filepath.write_text(yaml_content)
                    
                    progress.log_success(f"Successfully processed prompt {i} → {filepath}")
                    results[prompt] = str(filepath)
                    
                except Exception as e:
                    error_msg = f"Error processing prompt {i}: {str(e)}"
                    progress.log_error(error_msg)
                    logger.error(error_msg, exc_info=self.verbose)
                    results[prompt] = f"ERROR: {str(e)}"
        
        # Log final summary
        success_count = sum(1 for r in results.values() if not r.startswith("ERROR:"))
        if self.verbose:
            logger.info(f"Batch processing complete: {success_count}/{len(prompts)} prompts successful")
        
        return results

```

## File: prompt_storm/interfaces/service_interfaces.py

- Extension: .py
- Language: python
- Size: 1392 bytes
- Created: 2024-12-07 20:44:52
- Modified: 2024-12-07 20:44:52

### Code

```python
"""
Service interfaces for the prompt_storm package.
"""
from abc import ABC, abstractmethod

class OptimizerServiceInterface(ABC):
    """Interface for prompt optimization services."""
    
    @abstractmethod
    def optimize(self, prompt: str, **kwargs) -> str:
        """Optimize the given prompt."""
        pass

class YAMLServiceInterface(ABC):
    """Interface for YAML formatting services."""
    
    @abstractmethod
    def format_to_yaml(self, prompt: str, **kwargs) -> str:
        """Format the given prompt to YAML."""
        pass

class CSVServiceInterface(ABC):
    """Interface for CSV processing services."""
    
    @abstractmethod
    def read_prompts(self, csv_path: str, prompt_column: str) -> list[str]:
        """Read prompts from CSV file."""
        pass

class BatchOptimizerServiceInterface(ABC):
    """Interface for batch optimization services."""
    
    @abstractmethod
    def optimize_batch(
        self, 
        input_csv: str, 
        output_dir: str, 
        prompt_column: str
    ) -> dict[str, str]:
        """Optimize a batch of prompts from CSV and save to YAML files."""
        pass

class TranslationServiceInterface(ABC):
    """Interface for translation services."""
    
    @abstractmethod
    def translate(self, text: str, target_language: str) -> str:
        """Translate the given text to the target language."""
        pass


```

## File: pyproject.toml

- Extension: .toml
- Language: toml
- Size: 924 bytes
- Created: 2024-12-07 22:21:44
- Modified: 2024-12-07 22:21:44

### Code

```toml
[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.poetry]
name = "prompt-storm"
version = "0.1.0"
description = "A project for prompt engineering and generation"
authors = ["Your Name <your.email@example.com>"]
readme = "README.md"
packages = [{include = "prompt_storm"}]

[tool.poetry.dependencies]
python = ">=3.11,<4.0"
typer = ">=0.9.0"
rich = ">=10.0.0"
click = ">=8.0.0"
litellm = ">=1.0.0"
pydantic = ">=2.0.0"
python-dotenv = ">=1.0.0"
boto3 = "^1.35.76"

[tool.poetry.group.dev.dependencies]
ruff = "*"
black = "*"
pytest = "*"
pytest-mock = "*"
pytest-cov = "*"
pytest-asyncio = "*"

[tool.poetry.scripts]
prompt-storm = "prompt_storm.cli:cli"

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.black]
line-length = 88
target-version = ['py311']

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=prompt_storm --cov-report=term-missing"

```

## File: tests/test_optimizer.py

- Extension: .py
- Language: python
- Size: 5844 bytes
- Created: 2024-12-07 12:56:50
- Modified: 2024-12-07 12:56:50

### Code

```python
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

```

## File: tests/conftest.py

- Extension: .py
- Language: python
- Size: 390 bytes
- Created: 2024-12-07 10:31:47
- Modified: 2024-12-07 10:31:47

### Code

```python
"""Pytest configuration for async tests."""
import pytest
import asyncio
import sys

@pytest.fixture(scope="function")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()
    asyncio.set_event_loop(None)

```

## File: tests/test_placeholder.py

- Extension: .py
- Language: python
- Size: 262 bytes
- Created: 2024-12-06 10:23:29
- Modified: 2024-12-06 10:23:29

### Code

```python
def test_placeholder():
    """
    A placeholder test to ensure the testing framework is working.
    
    This test will always pass and serves as a basic sanity check
    for the project's testing setup.
    """
    assert True, "Basic test setup is working"

```

## File: tests/test_cli.py

- Extension: .py
- Language: python
- Size: 8234 bytes
- Created: 2024-12-06 13:27:37
- Modified: 2024-12-06 13:27:37

### Code

```python
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

```


