# Prompt Storm

Welcome to Prompt Storm, an advanced toolkit for prompt engineering and generation.

## Prerequisites

- Python 3.11+
- `uv` for dependency management

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/prompt-storm.git
   cd prompt-storm
   ```

2. Set up the virtual environment and install dependencies:
   ```bash
   uv venv .venv
   source .venv/bin/activate
   uv install
   ```

## Running the Program

To run the Prompt Storm CLI, use the following command:

```bash
python -m prompt_storm.main --help
```

This will display the help message with available options and commands.

## Running Tests

To run the test suite, execute:

```bash
PYTHONPATH=. pytest tests
```

This will run all tests and display the results, ensuring everything is working as expected.

## Contributing

Feel free to contribute by opening issues or submitting pull requests. We welcome improvements and new features!

## License

This project is licensed under the MIT License.
