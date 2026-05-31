"""Visualization generation engine utilizing an in-memory Matplotlib backend.

Renders high-quality line graphs and bar metrics, transforming binary image buffers
into layout-ready web assets via Base64 encoding.
"""

import base64
import io
import matplotlib
# Enforce a non-interactive server-safe GUI environment context
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from exceptions import InvalidInputError


def plot_trend(df: pd.DataFrame, country: str, metric: str) -> str:
    """Generates an in-memory line chart showing 7-day trends for a metric.

    Args:
        df (pd.DataFrame): The pre-processed global pandas dataset.
        country (str): Target geographical nation name.
        metric (str): Chosen data property filter ('new_cases' or 'new_deaths').

    Returns:
        str: UTF-8 decoded Base64 text string of the PNG image asset.

    Raises:
        InvalidInputError: If parameters fall outside validated lists.
    """
    # Validation boundary testing checks
    country_df = df[df['location'] == country]
    if country_df.empty:
        raise InvalidInputError(f"Target country '{country}' was not found in active frame.")

    plt.figure(figsize=(10, 5))

    try:
        if metric == 'new_cases':
            plt.plot(
                country_df['date'], 
                country_df['rolling_new_cases'], 
                color='blue', 
                label='7-Day Avg New Cases'
            )
            plt.ylabel('New Cases Daily Count')
        elif metric == 'new_deaths':
            # Dynamic processing calculation of matching deaths moving metrics
            rolling_deaths = country_df['new_deaths'].rolling(7, min_periods=1).mean()
            plt.plot(
                country_df['date'], 
                rolling_deaths, 
                color='red', 
                label='7-Day Avg New Deaths'
            )
            plt.ylabel('New Deaths Daily Count')
        else:
            raise InvalidInputError(f"Requested evaluation metric '{metric}' is unauthorized.")

        plt.title(f'COVID-19 Historical Wave Trend: {country}')
        plt.xlabel('Date Timeline')
        plt.legend(loc='upper left')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()

        # Save plotting buffer using structural Byte Streams
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=100)
        img_buffer.seek(0)
        base64_string = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    finally:
        # Guarantee closure cleanup sequence to fully prevent memory leakage issues
        plt.close()

    return base64_string


def plot_compare(df: pd.DataFrame) -> str:
    """Generates an in-memory comparative bar chart tracking peak deaths.

    Args:
        df (pd.DataFrame): The pre-processed global pandas dataset.

    Returns:
        str: UTF-8 decoded Base64 text string of the PNG bar visual asset.
    """
    plt.figure(figsize=(10, 6))

    try:
        # Analytical metric aggregation tracking peak historic deaths
        max_deaths = (
            df.groupby('location')['total_deaths']
            .max()
            .sort_values(ascending=False)
        )

        max_deaths.plot(kind='bar', color='indigo', edgecolor='black')
        plt.title('Total Historic COVID-19 Cumulative Casualties Comparison')
        plt.xlabel('Tracked National Framework Jurisdictions')
        plt.ylabel('Maximum Aggregate Death Metric')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle=':', alpha=0.5)
        plt.tight_layout()

        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=100)
        img_buffer.seek(0)
        base64_string = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    finally:
        plt.close()

    return base64_string