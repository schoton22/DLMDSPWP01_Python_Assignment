%%writefile src/database_manager.py
"""
Database Management Module
Handles SQLite database creation and data persistence using SQLAlchemy.
"""

import pandas as pd
from sqlalchemy import create_url, create_engine, Column, Float, Integer, MetaData, Table
from sqlalchemy.orm import declarative_base, sessionmaker
from src.exceptions import FileNotFoundException

# Define the Base class for SQLAlchemy models
Base = declarative_base()

class DatabaseManager:
    """
    Manages the connection and data operations for the SQLite database.
    """
    
    def __init__(self, db_name="assignment_database.db"):
        """
        Initializes the database engine and session.
        :param db_name: Name of the SQLite database file.
        """
        self.engine = create_engine(f"sqlite:///{db_name}")
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData()

    def load_csv_to_sqlite(self, file_path, table_name):
        """
        Loads data from a CSV file into a specific SQLite table.
        :param file_path: Path to the CSV source file.
        :param table_name: Destination table name in the database.
        :raises FileNotFoundException: If the CSV file is missing.
        """
        try:
            df = pd.read_csv(file_path)
            
            # This handles table creation and data insertion automatically
            df.to_sql(table_name, self.engine, if_exists='replace', index=False)
            print(f"Successfully loaded {file_path} into table '{table_name}'.")
            
        except FileNotFoundError:
            raise FileNotFoundException(file_path)
        except Exception as e:
            print(f"An unexpected error occurred while loading {file_path}: {e}")

    def get_engine(self):
        """Returns the SQLAlchemy engine instance."""
        return self.engine