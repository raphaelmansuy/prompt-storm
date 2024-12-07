"""
Response models for the prompt_storm package.
"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class YAMLValidationError:
    """Represents a YAML validation error."""
    message: str
    line: Optional[int] = None
    column: Optional[int] = None
