# Prompt Storm

Welcome to Prompt Storm, an advanced toolkit for prompt engineering and generation. This tool helps you optimize and enhance your prompts using state-of-the-art language models.

## Features

- **Prompt Optimization**: Enhance your prompts using advanced language models
- **Model Selection**: Choose from different LLM models for optimization
- **File Support**: Read prompts from files and save optimized results
- **Configurable**: Adjust temperature and token limits for better results
- **Extensible**: Built with a modular design for easy feature additions

## Prerequisites

- Python 3.11+
- Poetry (for dependency management)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/prompt-storm.git
   cd prompt-storm
   ```

2. Install dependencies with Poetry:
   ```bash
   poetry install
   ```

## Usage

Prompt Storm provides a powerful CLI for prompt optimization. Here are some common use cases:

### Basic Prompt Optimization
```bash
poetry run prompt-storm optimize "Your prompt here"
```

### Using Different Models
```bash
poetry run prompt-storm optimize --model gpt-3.5-turbo "Your prompt"
```

### Adjusting Generation Parameters
```bash
poetry run prompt-storm optimize \
  --temperature 0.8 \
  --max-tokens 1000 \
  "Your prompt"
```

### File Operations
```bash
# Read prompt from file
poetry run prompt-storm optimize --input-file input.txt

# Save optimized prompt to file
poetry run prompt-storm optimize \
  "Your prompt" \
  --output-file optimized.txt
```

### Getting Help
```bash
poetry run prompt-storm --help
poetry run prompt-storm optimize --help
```

## Development

### Setting Up Development Environment
```bash
# Install all dependencies including development tools
poetry install
```

### Running Tests
```bash
# Run tests with coverage report
poetry run pytest

# Run specific test file
poetry run pytest tests/test_cli.py
```

### Code Quality
```bash
# Format code
poetry run black .

# Run linter
poetry run ruff .
```

### Building Package
```bash
poetry build
```

## Project Structure

```
prompt-storm/
├── prompt_storm/        # Main package directory
│   ├── __init__.py
│   ├── cli.py          # CLI implementation
│   └── optimizer.py    # Prompt optimization logic
├── tests/              # Test directory
│   └── test_*.py       # Test files
├── pyproject.toml      # Project configuration
└── README.md          # This file
```

## Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests to ensure everything works
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License. See the LICENSE file for details.
