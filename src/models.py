%%writefile src/models.py
"""
This module defines the class hierarchy for functions.
"""
import pandas as pd

class Function:
    """
    Base class representing a mathematical function dataset.
    Demonstrates inheritance as required by the assignment guidelines.
    """
    def __init__(self, data: pd.DataFrame):
        self.data = data

class TrainingFunction(Function):
    """Represents the four training datasets."""
    pass

class IdealFunction(Function):
    """Represents the fifty ideal functions provided."""
    pass