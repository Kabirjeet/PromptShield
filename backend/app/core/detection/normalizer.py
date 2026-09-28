
import re
import unicodedata


def normalize_text(text: str) -> str:
    """
    Normalize user input before security analysis.

    This function does not determine whether the input
    is malicious. It only creates a consistent representation.
    """

    if not text:
        return ""

    # Normalize Unicode characters into a canonical representation.
    text = unicodedata.normalize("NFKC", text)

    # Convert to lowercase.
    text = text.lower()

    # Replace repeated whitespace with a single space.
    text = re.sub(r"\s+", " ", text)

    # Remove leading/trailing whitespace.
    text = text.strip()

    return text