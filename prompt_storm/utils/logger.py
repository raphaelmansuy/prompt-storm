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
