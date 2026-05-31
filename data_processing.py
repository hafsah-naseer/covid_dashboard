"""Data processing module for loading and manipulating the OWID COVID-19 dataset.

Handles initial file operations, structural column validation, list filtering,
and window-based transformations.
"""

import pandas as pd
from exceptions import DataNotFoundError

# Definition of the targeted 10 countries tracking constraint
COUNTRIES = [
    'United States', 'India', 'Brazil', 'France', 'Germany',
    'United Kingdom', 'Italy', 'South Korea', 'Japan', 'Canada'
]


def load_and_clean_data(filepath: str) -> pd.DataFrame:
    """Loads the OWID raw CSV dataset and performs rolling analytical aggregations.

    Args:
        filepath (str): The absolute or relative system path to the dataset.

    Returns:
        pd.DataFrame: A fully cleaned, sorted, and aggregated dataset.

    Raises:
        DataNotFoundError: If the CSV file is missing or has bad formatting.
    """
    required_columns = [
        'location', 'date', 'new_cases', 
        'new_deaths', 'total_cases', 'total_deaths'
    ]

    try:
        # File I/O for data persistence tracking
        df = pd.read_csv(filepath, usecols=required_columns, parse_dates=['date'])
    except FileNotFoundError as err:
        raise DataNotFoundError(
            f"Critical Error: The source file '{filepath}' was not found."
        ) from err
    except ValueError as err:
        raise DataNotFoundError(
            "Critical Error: The dataset schema is missing essential columns."
        ) from err

    try:
        # Filter dataframe rows using explicit list constraint
        filtered_df = df[df['location'].isin(COUNTRIES)].copy()

        # Sort values sequentially for accurate sequential rolling window math
        filtered_df = filtered_df.sort_values(by=['location', 'date'])

        # Compute the 7-day rolling average of daily new cases per country grouping
        filtered_df['rolling_new_cases'] = (
            filtered_df.groupby('location')['new_cases']
            .transform(lambda x: x.rolling(window=7, min_periods=1).mean())
        )
    except Exception as err:
        raise DataNotFoundError(
            f"An unexpected data transformation error occurred: {str(err)}"
        ) from err

    return filtered_df