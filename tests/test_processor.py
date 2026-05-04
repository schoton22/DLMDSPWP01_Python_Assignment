"""
Unit Testing Module
Validates the mathematical accuracy of the DataProcessor class.
"""

import unittest
import pandas as pd
import numpy as np
from src.data_processor import DataProcessor

class TestDataProcessor(unittest.TestCase):
    """Tests for Least-Squares selection and mapping logic."""

    def setUp(self):
        """Set up a small dummy dataset for testing."""
        self.train_df = pd.DataFrame({
            'x': [1, 2],
            'y1': [10, 20]
        })
        self.ideal_df = pd.DataFrame({
            'x': [1, 2],
            'y_ideal_1': [10.1, 20.1], # Close fit
            'y_ideal_2': [50, 60]      # Poor fit
        })
        self.processor = DataProcessor(self.train_df, self.ideal_df)

    def test_selection_logic(self):
        """Ensure the processor selects the function with the lowest SSR."""
        chosen = self.processor.select_four_ideal_functions()
        # y1 should match y_ideal_1
        self.assertEqual(chosen['y1']['ideal_column'], 'y_ideal_1')

if __name__ == '__main__':
    unittest.main()