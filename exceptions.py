"""Custom exception classes for the COVID-19 Dashboard application.

This module provides clear, descriptive errors that help prevent 
the Flask application from crashing during unexpected operational runtime anomalies.
"""

class DashboardError(Exception):
    """Base exception class for all custom dashboard errors."""
    pass


class DataNotFoundError(DashboardError):
    """Exception raised when the raw data file or its required schema is missing."""
    pass


class InvalidInputError(DashboardError):
    """Exception raised when a user requests an invalid country or metric."""
    pass