"""
Data Processing Module
Provides computational logic for function selection and test data mapping.
This module handles the Least-Squares calculations and threshold mapping.
"""

import pandas as pd
import numpy as np

class DataProcessor:
    """
    Handles the computational logic for function selection and data mapping.
    """
    
    def __init__(self, training_data: pd.DataFrame, ideal_functions: pd.DataFrame):
        """
        Initializes the processor with datasets.
        :param training_data: DataFrame containing the four training functions.
        :param ideal_functions: DataFrame containing the fifty ideal functions.
        """
        self.training_data = training_data
        self.ideal_functions = ideal_functions
        self.selected_functions = {}

    def select_four_ideal_functions(self):
        """
        Identifies the four ideal functions that minimize the sum of squared deviations (Least-Square criterion) for the training data.
        :return: Dictionary with chosen function names and their max training deviations.
        """
        train_cols = [col for col in self.training_data.columns if col != 'x']
        ideal_cols = [col for col in self.ideal_functions.columns if col != 'x']
        
        for t_col in train_cols:
            best_ssr = float('inf')
            best_fit_name = None
            max_dev_train = 0
            
            for i_col in ideal_cols:
                # Calculate squared residuals: (y_train - y_ideal)^2
                residuals = self.training_data[t_col] - self.ideal_functions[i_col]
                ssr = (residuals**2).sum()
                
                if ssr < best_ssr:
                    best_ssr = ssr
                    best_fit_name = i_col
                    max_dev_train = residuals.abs().max()
            
            self.selected_functions[t_col] = {
                'ideal_column': best_fit_name,
                'max_deviation': max_dev_train
            }
            
        return self.selected_functions

    def map_test_data(self, test_data: pd.DataFrame):
        """
        Maps test points to the selected ideal functions if the deviation is within the max_deviation * sqrt(2) threshold.
        :param test_data: DataFrame containing x and y test pairs.
        :return: DataFrame containing mapped results and deviations.
        """
        results = []
        threshold_factor = np.sqrt(2)
        
        for _, row in test_data.iterrows():
            x_val, y_val = row['x'], row['y']
            best_mapping = None
            min_deviation = float('inf')
            
            for train_col, info in self.selected_functions.items():
                ideal_col = info['ideal_column']
                # Retrieve the ideal y-value for the corresponding x-coordinate
                ideal_val = self.ideal_functions.loc[self.ideal_functions['x'] == x_val, ideal_col].values[0]
                
                deviation = abs(y_val - ideal_val)
                max_allowed = info['max_deviation'] * threshold_factor
                
                # Criterion: Deviation <= max training deviation * sqrt(2)
                if deviation <= max_allowed:
                    if deviation < min_deviation:
                        min_deviation = deviation
                        best_mapping = ideal_col
            
            results.append({
                'x': x_val,
                'y': y_val,
                'delta_y': min_deviation if best_mapping else None,
                'ideal_function_no': best_mapping
            })
            
        return pd.DataFrame(results)