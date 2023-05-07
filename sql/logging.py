"""
Log API requests to a SQL Server database

Modules:
    3rd Party: traceback, datetime
    Custom: config

Classes:

    LogEntries
        Log entries to the SQL Server database

Functions

    None

Exceptions:

    None

Misc Variables:

    None

Limitations/Requirements:
    None

Author:
    Luke Robertson - May 2023
"""

import traceback as tb
from datetime import datetime

import config
import sql.sql as sql


class LogEntries:
    """
    Log entries to the SQL Server database

    Supports being instantiated with the 'with' statement

    Attributes
    ----------
    TBA

    Methods
    -------
    log_request(source, endpoint, headers, req_body, return_code, error)
        Adds a log entry to the SQL Server database
    """

    def __init__(self):
        """
        Class constructor

        Get the logging DB connection details from config file

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        None
        """

        self.server = config.SQL_SERVER['db_server']
        self.database = config.SQL_SERVER['db_name']
        self.table = config.SQL_SERVER['log_table']

    def __enter__(self):
        """
        Called when the 'with' statement is used

        Calls the 'connect' method to connect to the server

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        self
            The instantiated object
        """

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Called when the 'with' statement is finished

        Calls the 'disconnect' method to gracefully close the connection
            to the server

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        self
            None
        """

        # handle errors that were raised
        if exc_type:
            print(
                f"Exception of type {exc_type.__name__} occurred: {exc_value}"
            )
            if traceback:
                print("Traceback:")
                print(tb.format_tb(traceback))

    def log_request(
            self,
            source,
            endpoint,
            headers,
            req_body,
            return_code,
            error,
            method
    ):
        """
        Adds a log entry to the SQL Server database

        Parameters
        ----------
        TBA

        Raises
        ------
        None

        Returns
        -------
        True : bool
            If there were no errors
        False : bool
            If there were errors
        """

        # Collect the fields to write to SQL
        date = datetime.now().date()
        time = datetime.now().time().strftime("%H:%M:%S")

        # Create a dictionary of the values to insert
        values = {
            'logdate': date,
            'logtime': time,
            'src': source,
            'endpoint': endpoint,
            'method': method,
            'headers': headers,
            'req_body': req_body,
            'return_code': return_code,
            'error': error
        }

        # Connect to the database and add a new device record
        with sql.SqlServer(
            server=self.server,
            db=self.database,
            table=self.table
        ) as log_sql:
            output = log_sql.add(
                fields=values,
            )

        # If there was an error, return it
        if not output:
            return False

        return True
