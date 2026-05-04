%%writefile src/exceptions.py
"""
Custom Exception Module
This module defines specific exceptions to handle errors during data loading and mathematical processing.
"""

class DataError(Exception):
    """Base class for exceptions in this module."""
    pass

class FileNotFoundException(DataError):
    """Raised when a required CSV file is missing."""
    def __init__(self, filename):
        self.message = f"Critical Error: The file '{filename}' was not found in the /data directory."
        super().__init__(self.message)

class MappingLimitReachedException(DataError):
    """Raised when test data exceeds the mapping criteria threshold."""
    pass