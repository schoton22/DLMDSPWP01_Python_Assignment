# DLMDSPWP01_Python_Assignment
# Automated Selection of Ideal Functions

**Author:** Anton Scholz  
**Matriculation Number:** IU14162303  
**Module:** Python Programming (DLMDSPWP01)

## Project Description
This application automates the process of identifying the best-fitting mathematical models for training datasets from a pool of candidate "ideal" functions. The selection is based on minimizing the Sum of Squared Residuals (SSR). Once models are selected, test data is mapped to these functions using a strict statistical threshold ($max\_dev_{train} \times \sqrt{2}$).

## Features
- **Modular OOP Architecture:** Clean separation of data processing, database management, and visualization.
- **Relational Persistence:** Utilizes SQLAlchemy and SQLite for structured data storage.
- **Interactive Visualization:** Generates a web-based dashboard using Bokeh to analyze fits and outliers.
- **Unit Testing:** Includes automated tests to verify mathematical accuracy.

## Project Structure
- `main.py`: The central entry point for the application.
- `src/`: Internal modules (data processor, database manager, visualizer, custom exceptions).
- `data/`: Local storage for `train.csv`, `ideal.csv`, and `test.csv`.
- `tests/`: Unit tests for the core logic.
- `assignment_database.db`: The SQLite database generated upon execution.
- `results_visualization.html`: Interactive diagnostic plots.
