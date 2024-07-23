"""
This module contains functions to convert text from one language to another.
"""

def convert_mandarin(text: str):
    """
    Convert the provided text from garbled Chinese simplified to readable Chinese simplified
    Returns: String of the converted text
    """
    cp936_bytes = text.encode('latin-1')  # Encode to bytes using latin-1
    utf16_bytes = cp936_bytes.decode('cp936').encode('utf-16')  # Decode CP936 and encode to UTF-16
    result = utf16_bytes.decode('utf-16')
    return result
