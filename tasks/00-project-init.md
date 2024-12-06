## Who you are:

- Your are an expert in software engineering
- Expert with the following tools:
    - Python 3.11
    - Git
    - Docker
    - uv 
    - pytest
    - pydantic
    - fastapi
    - uv 
    - litellm 

## Development Tools Configuration

### Ruff
- Static code analysis and linting
- Replaces multiple tools (flake8, isort, pydocstyle, etc.)
- Fast and extremely low-overhead

### Black
- Uncompromising code formatter
- Ensures consistent code style
- No configuration required

### Pytest
- Modern testing framework
- Supports simple and complex testing scenarios
- Easy test discovery and execution

### Recommended Configuration

1. Install tools:
```bash
pip install ruff black pytest
```

2. Create configuration files:
- `pyproject.toml`: Configure tools
- `.gitignore`: Exclude unnecessary files
- `tests/`: Directory for test files

3. Add scripts to `pyproject.toml`:
```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.black]
line-length = 88
target-version = ['py311']

[tool.pytest.ini_options]
testpaths = ["tests"]
```

4. Pre-commit hooks (optional but recommended):
- Automate code quality checks
- Ensure consistent code style before commits

## Task to perform:


- Create a virtual environment
- Scaffold the project prompt-storm
- Add the following tools to the project:
    - Ruff
    - Black
    - Pytest


