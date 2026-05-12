"""
Main Entry Point
Final integration
Executes data loading, math processing, persistence, and visualization.
"""

import os
import pandas as pd
from src.database_manager import DatabaseManager
from src.data_processor import DataProcessor
from src.visualizer import Visualizer

def main():
    # Paths
    train_path = os.path.join("data", "train.csv")
    ideal_path = os.path.join("data", "ideal.csv")
    test_path = os.path.join("data", "test.csv")
    
    # 1. Data Ingestion
    db_manager = DatabaseManager()
    db_manager.load_csv_to_sqlite(train_path, "training_data")
    db_manager.load_csv_to_sqlite(ideal_path, "ideal_functions")
    
    # Load into memory for processing
    engine = db_manager.get_engine()
    train_df = pd.read_sql_table("training_data", engine)
    ideal_df = pd.read_sql_table("ideal_functions", engine)
    test_df = pd.read_csv(test_path) # Direct read for line-by-line processing later
    
    # 2. Function Selection (Least-Squares)
    processor = DataProcessor(train_df, ideal_df)
    chosen_functions = processor.select_four_ideal_functions()
    
    print("\n--- Selection Results ---")
    for t_col, res in chosen_functions.items():
        print(f"Training {t_col} -> Ideal {res['ideal_column']} (Max Train Dev: {res['max_deviation']:.4f})")
    
    # 3. Test Data Mapping (sqrt(2) criterion)
    mapped_test_results = processor.map_test_data(test_df)
    print(f"Number of mapped points: {len(mapped_test_results[mapped_test_results['ideal_function_no'].notnull()])}")
    # 4. Persistence
    db_manager.save_dataframe_to_table(mapped_test_results, "test_data_mappings")
    
    # 5. Visualization
    viz = Visualizer()
    viz.plot_results(train_df, ideal_df, chosen_functions, mapped_test_results)

if __name__ == "__main__":
    main()
