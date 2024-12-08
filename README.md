# Prompt Storm: Advanced Prompt Engineering Toolkit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Prompt Storm is a powerful toolkit designed for sophisticated prompt engineering and optimization. It provides a comprehensive set of tools for creating, optimizing, and managing prompts at scale, making it an essential tool for AI developers and researchers working with language models.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
  - [Command Usage Examples](#command-usage-examples)
- [Architecture](#architecture)
- [API Reference](#api-reference)
- [Development](#development)
- [Advanced Topics](#advanced-topics)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Contributing](#contributing)
- [Publishing to PyPI](#publishing-to-pypi)

## Overview

Prompt Storm empowers developers to:

- Optimize prompts for better performance and consistency
- Process multiple prompts in batch mode
- Format prompts in standardized YAML format
- Track optimization progress with rich logging
- Handle errors gracefully with comprehensive error reporting

### Key Features

- **Intelligent Prompt Optimization**: Leverages advanced LLMs to enhance prompt effectiveness
- **Batch Processing**: Efficiently handle multiple prompts using CSV input
- **YAML Formatting**: Standardize prompts with structured YAML output
- **Progress Tracking**: Rich console output with detailed progress information
- **Error Handling**: Robust error management with helpful error messages

### Use Cases

- Optimizing prompts for chatbots and AI assistants
- Standardizing prompt formats across large projects
- Processing and converting legacy prompts to YAML format
- Batch optimization of prompt libraries
- Quality assurance for prompt engineering pipelines

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Basic Installation

```bash
pip install prompt-storm
```

### Development Setup

```bash
git clone https://github.com/yourusername/prompt-storm.git
cd prompt-storm
pip install -e ".[dev]"
```

### Dependencies

- click: Command line interface creation
- rich: Enhanced terminal output
- litellm: LLM interface
- pyyaml: YAML processing
- pandas: CSV handling

## Quick Start

### Basic Usage

Optimize a single prompt:

```bash
prompt-storm optimize "Write a story about {{subject}}"
```

Result:

```text
Write a detailed and engaging story about {{subject_name}}. Ensure the narrative includes:
1. A clear introduction to {{subject_name}} and their background.
2. A central conflict or challenge that {{subject_name}} faces.
3. The steps {{subject_name}} takes to address the conflict, using Chain of Thought (CoT) to explain their reasoning.
4. Interactions with other characters to provide depth and context.
5. A resolution that is satisfying and aligns with the character's journey.
6. Consider diverse perspectives and avoid stereotypes.
7. Maintain a balance between creative freedom and factual accuracy if {{subject_name}} is based on a real person or event.
8. Use vivid, descriptive language to enhance the reader's experience.
```

Example with yaml output:

```bash
prompt-storm optimize "Write a story about {{subject}}" --yaml
```

Result:

```yaml
name: "Adventure Story Prompt"
version: '1.0'
description: >-
  A prompt designed to generate a compelling story about a main character who embarks on an unexpected adventure. The story should include details about the conflict they face and how 
they resolve it, reflecting diverse perspectives and addressing potential biases. The narrative style should balance human emotion with logical progression.
author: quantalogic
input_variables:
  main_character:
    type: string
    description: >-
      The name or description of the main character in the story.
    examples:
      - "Alice"
      - "John Doe"
  setting:
    type: string
    description: >-
      The environment or location where the adventure takes place.
    examples:
      - "a mystical forest"
      - "a futuristic city"
  conflict:
    type: string
    description: >-
      The main challenge or problem the character faces during their adventure.
    examples:
      - "a quest to find a lost artifact"
      - "battling a powerful enemy"
tags:
  - "storytelling"
  - "adventure"
  - "character development"
  - "conflict resolution"
categories:
  - "writing"
  - "creative storytelling"
content: >-
  Write a compelling story about {{main_character}} who embarks on an unexpected adventure in {{setting}}. Include details about {{conflict}} they face and how they resolve it. Ensure the
story reflects diverse perspectives and addresses potential biases. Use a narrative style that balances human emotion with logical progression. For example, start with an introduction of 
{{main_character}} and their initial situation, followed by the emergence of {{conflict}}, their journey through challenges, and finally, the resolution. Consider edge cases such as 
unexpected outcomes or alternative resolutions. Maintain clear, unambiguous language throughout.
```

Process multiple prompts from a CSV file:

```bash
prompt-storm optimize-batch input.csv output_dir --prompt-column "prompt"
```

Format a prompt to YAML:

```bash
prompt-storm format-prompt "Generate a creative story" --output-file story.yaml
```

## Usage Guide

### Command Line Interface

#### optimize

Optimize a single prompt with customizable parameters:

```bash
prompt-storm optimize "Your prompt" \
    --model gpt-4o-mini \
    --max-tokens 2000 \
    --temperature 0.7 \
    --output-file optimized.yaml
```

Parameters:

- `--model`: LLM model to use (default: gpt-4o-mini)
- `--max-tokens`: Maximum tokens in response (default: 2000)
- `--temperature`: Generation temperature (default: 0.7)
- `--input-file`: Optional input file containing the prompt
- `--output-file`: Optional output file for the result
- `--verbose`: Enable detailed logging

#### optimize-batch

Process multiple prompts from a CSV file:

```bash
prompt-storm optimize-batch prompts.csv output/ \
    --prompt-column "prompt" \
    --model gpt-4o-mini \
    --language english
```

Parameters:

- `input-csv`: Path to input CSV file
- `output-dir`: Directory for output files
- `--prompt-column`: Name of CSV column containing prompts
- `--model`: LLM model to use
- `--language`: Target language for optimization

#### format-prompt

Convert a prompt to YAML format:

```bash
prompt-storm format-prompt "Your prompt" \
    --output-file formatted.yaml \
    --language english
```

### Command Usage Examples

#### Example 1: Optimizing a Single Prompt with Specific Parameters

```bash
prompt-storm optimize "Explain the concept of quantum computing" \
    --model gpt-4o-turbo \
    --max-tokens 1500 \
    --temperature 0.5 \
    --output-file quantum_computing_explanation.yaml
```

#### Example 2: Batch Processing of Prompts from a CSV File

```bash
prompt-storm optimize-batch prompts.csv output/ \
    --prompt-column "description" \
    --model gpt-4o-mini \
    --language english
```

#### Example 3: Formatting a Prompt to YAML

```bash
prompt-storm format-prompt "Create a recipe for chocolate cake" \
    --output-file chocolate_cake_recipe.yaml
```

#### Example 4: Optimizing a Prompt with Detailed Logging

```bash
prompt-storm optimize "Design a user-friendly interface for a mobile app" \
    --model gpt-4o-mini \
    --max-tokens 2000 \
    --temperature 0.7 \
    --verbose
```

#### Example 5: Batch Processing with Specific Language

```bash
prompt-storm optimize-batch prompts.csv output/ \
    --prompt-column "description" \
    --model gpt-4o-mini \
    --language spanish
```

### Configuration

Model configuration options:

```python
config = OptimizationConfig(
    model="gpt-4o-mini",
    max_tokens=2000,
    temperature=0.7,
    language="english"
)
```

### Supported models

We use [litellm](https://docs.litellm.ai/) to interface with various language models.

Example of models:

#### OpenAI models

- `gpt-4o-mini`: GPT-4o Mini model
- `gpt-4o-turbo`: GPT-4o Turbo model

#### AWS Bedrock models

- `bedrock/amazon.nova-pro-v1:0`
- `bedrock/amazon.nova-lite-v1:0`
- `bedrock/amazon.nova-micro-v1:0`
- `bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0`

## Ollama models

- `ollama/llama3.3:latest`
- `ollama/qwen2.5-coder:14b`

## Architecture

### Component Overview

```mermaid
graph TD
    A[CLI] --> B[Optimizer]
    B --> C[Services]
    C --> D[YAML Service]
    C --> E[CSV Service]
    C --> F[Batch Service]
    B --> G[Utils]
    G --> H[Logger]
    G --> I[Error Handler]
    G --> J[Response Processor]
```

### Core Services

#### OptimizerService

Handles prompt optimization using LLMs:

```python
optimizer = OptimizerService(config)
result = optimizer.optimize("Your prompt")
```

#### YAMLService

Manages YAML formatting and validation:

```python
yaml_service = YAMLService(config)
yaml_output = yaml_service.format_to_yaml(prompt)
```

#### BatchOptimizerService

Processes multiple prompts efficiently:

```python
batch_service = BatchOptimizerService(
    optimizer_service=optimizer,
    yaml_service=yaml_service,
    csv_service=csv_service
)
```

## Development

### Project Structure

```text
prompt_storm/
├── __init__.py          # Package initialization
├── cli.py              # Command line interface
├── optimizer.py        # Core optimization logic
├── models/            # Data models
│   ├── config.py
│   └── responses.py
├── services/          # Core services
│   ├── optimizer_service.py
│   ├── yaml_service.py
│   ├── csv_service.py
│   └── batch_optimizer_service.py
├── utils/            # Utility functions
│   ├── logger.py
│   ├── error_handler.py
│   └── response_processor.py
└── interfaces/       # Service interfaces
    └── service_interfaces.py
```

### Testing

Run the test suite:

```bash
pytest tests/
```

Write tests following the existing pattern:

```python
def test_optimize():
    optimizer = PromptOptimizer()
    result = optimizer.optimize("Test prompt")
    assert result is not None
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## Advanced Topics

### Custom Configurations

```python
from prompt_storm.models.config import OptimizationConfig

config = OptimizationConfig(
    model="gpt-4o-mini",
    max_tokens=2000,
    temperature=0.7,
    language="english"
)
```

### Integration Example

```python
from prompt_storm import PromptOptimizer

optimizer = PromptOptimizer()

# Single prompt optimization
result = optimizer.optimize("Your prompt")

# Batch processing
with open('prompts.csv', 'r') as f:
    prompts = f.readlines()
    results = [optimizer.optimize(p) for p in prompts]
```

### Best Practices

1. Use appropriate temperature settings for your use case
2. Implement proper error handling
3. Monitor token usage
4. Validate YAML output
5. Use batch processing for large datasets

## Troubleshooting

### Common Issues

1. Rate Limiting

```python
try:
    result = optimizer.optimize(prompt)
except Exception as e:
    if "rate limit" in str(e).lower():
        time.sleep(60)  # Wait before retry
```

2. Invalid YAML Format

```python
try:
    yaml_output = yaml_service.format_to_yaml(prompt)
except YAMLValidationError as e:
    logger.error(f"YAML validation failed: {e}")
```

### Error Messages

- `Rate limit exceeded`: Wait a few minutes or upgrade API plan
- `Invalid YAML format`: Check prompt structure and formatting
- `Resource exhausted`: Reduce batch size or implement rate limiting
- `Invalid model`: Verify model name and availability

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.

## Contributing
We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Credits

Developed by the Prompt Storm team. Special thanks to all contributors.

## Publishing to PyPI

To publish the project to PyPI using Poetry, follow these steps:

### 1. Update Version

Update the version number in `pyproject.toml`.

### 2. Log in to PyPI

Log in to PyPI using your token:

```bash
poetry config pypi-token.pypi <your-pypi-token>
```

### 3. Build the Distribution

Build the source distribution and wheel:

```bash
poetry build
```

### 4. Upload to PyPI

Upload the distribution to PyPI using `twine`:

```bash
twine upload dist/*
```

### 5. Verify Upload

Verify the upload by checking the project page on PyPI.
