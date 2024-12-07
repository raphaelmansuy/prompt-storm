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
