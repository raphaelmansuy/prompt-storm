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
