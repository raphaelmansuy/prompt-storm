"""
Utility functions for processing responses.
"""
import re
from typing import Any

def strip_markdown(content: str) -> str:
    """Remove markdown code block markers from content."""
    content = content.strip()
    # Remove markdown code block markers with or without language specifier
    content = re.sub(r'^```\w*\s*\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'\n```\s*$', '', content, flags=re.MULTILINE)
    return content.strip()

def extract_content_from_completion(completion: Any) -> str:
    """Extract content from a completion response."""
    return completion.choices[0].message.content.strip()
