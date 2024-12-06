from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def create_app() -> typer.Typer:
    """
    Create and configure the Typer application.
    
    Returns:
        A configured Typer application instance.
    """
    app = typer.Typer(
        name="prompt-storm",
        help="Advanced Prompt Engineering Toolkit",
        rich_help_panel=True,
        no_args_is_help=True,
    )
    return app

def main(
    verbose: Optional[bool] = typer.Option(
        False, 
        "--verbose", 
        "-v", 
        help="Enable verbose logging"
    )
) -> None:
    """
    Main entry point for Prompt Storm CLI.
    
    Args:
        verbose: Enable detailed logging output
    """
    console.print(
        Panel(
            Text.assemble(
                ("Prompt Storm ", "bold green"),
                ("v0.1.0", "dim")
            ),
            title="🚀 Welcome",
            border_style="bold blue"
        )
    )
    
    if verbose:
        console.print("[bold yellow]Verbose mode enabled[/bold yellow]")

if __name__ == "__main__":
    app = create_app()
    app.command()(main)
    app()
