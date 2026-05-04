"""
Data Models Module
Defines the class hierarchy for different function types.
"""

import pandas as pd

class Function:
    """
    Base class representing a mathematical dataset.
    Attributes:
        data (pd.DataFrame): The x-y pairs for the function.
        name (str): Identifier for the function.
    """
    def __init__(self, data, name):
        self.data = data
        self.name = name

    def get_y_values(self, column_name):
        """Returns the y-values for a specific function column."""
        return self.data[column_name]

class TrainingFunction(Function):
    """
    Inherits from Function. Represents the four training datasets.
    """
    def __init__(self, data, name="Training Dataset"):
        super().__init__(data, name)

class IdealFunction(Function):
    """
    Inherits from Function. Represents the fifty ideal functions.
    """
    def __init__(self, data, name="Ideal Functions Pool"):
        super().__init__(data, name)