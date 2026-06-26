import re
from typing import Any, Dict
from datetime import datetime

def sanitize_text(text: str) -> str:
    """
    Sanitizes string inputs by stripping whitespace and removing harmful characters.
    """
    if not text:
        return ""
    # Strip leading/trailing whitespaces and reduce multiple spaces
    cleaned = re.sub(r'\s+', ' ', text.strip())
    return cleaned

def format_date_range(start_date: datetime, end_date: datetime | None) -> str:
    """
    Formats a professional career timeline date range (e.g., 'Jan 2020 - Present').
    """
    start_str = start_date.strftime("%b %Y")
    end_str = end_date.strftime("%b %Y") if end_date else "Present"
    return f"{start_str} - {end_str}"

def format_file_size(size_in_bytes: int) -> str:
    """
    Converts bytes into a human-readable file size string (e.g., '2.4 MB').
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.1f} {unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.1f} TB"

def safe_get_nested(data: Dict[str, Any], *keys: str, default: Any = None) -> Any:
    """
    Safely retrieves a nested value from a dictionary.
    Example: safe_get_nested(user_profile, 'experience', 'last_role', 'title')
    """
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current
