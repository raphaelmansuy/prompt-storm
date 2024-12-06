import sys
from pathlib import Path

# Add the prompt-storm directory to the Python path
sys.path.append(str(Path(__file__).resolve().parents[1] / 'prompt_storm'))

import pytest
from typer.testing import CliRunner
from prompt_storm.main import create_app, main

runner = CliRunner()
app = create_app()
app.command()(main)  # Register the main function as a command

def test_main_help():
    """Test the help command of the CLI."""
    result = runner.invoke(app, ['--help'])
    assert result.exit_code == 0
    # Check for key parts of the help message
    assert "Usage:" in result.output
    assert "[OPTIONS]" in result.output
    assert "--verbose" in result.output

def test_main_verbose():
    """Test the verbose flag of the CLI."""
    result = runner.invoke(app, ['--verbose'])
    assert result.exit_code == 0
    assert "Verbose mode enabled" in result.output
