"""
Connect to an SQL server/database/table

Performs read/write operations on the table
Supports using the 'with' statement

Modules:
    3rd Party: pyodbc, traceback
    Custom: None

Classes:

    SqlServer
        Defines a connection the SQL resource
        Performs read/write functions on the resource

Functions

    None

Exceptions:

    None

Misc Variables:

    None

Limitations/Requirements:
    None

Author:
    Luke Robertson - April 2023
"""


import pyodbc
import traceback as tb


class SqlServer:
    """
    Connect to an SQL server/database to read and write

    Supports being instantiated with the 'with' statement

    Attributes
    ----------
    server : str
        The SQL server hostname to connect to
    db : str
        The SQL database to connect to
    table : str
        The table to write to or read from

    Methods
    -------
    connect()
        Connect to an SQL server
    disconnect()
        Gracefully disconnect from the server
    create_table()
        Create a table
    add()
        Add a record
    delete()
        Delete a record
    """

    def __init__(self, server, db, table):
        """
        Class constructor

        Gets the SQL server/db/table names
        Sets up empty connection and cursor objects

        Parameters
        ----------
        server : str
            The server name
        db : str
            The database name
        table : str
            The table name

        Raises
        ------
        None

        Returns
        -------
        None
        """

        self.server = server
        self.db = db
        self.table = table
        self.conn = None
        self.cursor = None

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

        self.connect()
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

        # Close the connection to the server
        self.disconnect()

        # handle errors that were raised
        if exc_type:
            print(
                f"Exception of type {exc_type.__name__} occurred: {exc_value}"
            )
            if traceback:
                print("Traceback:")
                print(tb.format_tb(traceback))

    def connect(self):
        """
        Connect to the SQL server

        Parameters
        ----------
        None

        Raises
        ------
        pyodbc.DataError
        pyodbc.OperationalError
        pyodbc.IntegrityError
        pyodbc.InternalError
        pyodbc.ProgrammingError
        pyodbc.NotSupportedError
        pyodbc.Error

        Returns
        -------
        None
        """

        # Connect to the server and database
        try:
            self.conn = pyodbc.connect(
                'Driver={SQL Server};'
                'Server=%s;'
                'Database=%s;'
                'Trusted_Connection=yes;'
                % (self.server, self.db))

        # Handle errors
        except pyodbc.DataError as e:
            raise Exception("A data error has occurred") from e

        except pyodbc.OperationalError as e:
            raise Exception(
                ("An operational error has occurred ",
                 "while connecting to the database")
            ) from e

        except pyodbc.IntegrityError as e:
            raise Exception("An Integrity error has occurred") from e

        except pyodbc.InternalError as e:
            raise Exception("An internal error has occurred") from e

        except pyodbc.ProgrammingError as e:
            if 'Cannot open database' in str(e):
                print("Unable to open the database")
                print("Make sure the name is correct, and credentials are ok")

            raise Exception("A programming error has occurred") from e

        except pyodbc.NotSupportedError as e:
            raise Exception("A 'not supported' error has occurred") from e

        except pyodbc.Error as e:
            raise Exception("A generic error has occurred") from e

        # If the connection was successful, create a cursor
        self.cursor = self.conn.cursor()

    def disconnect(self):
        """
        Gracefully close the connection to the server

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

        self.cursor.close()
        self.conn.close()

    def create_table(self, fields):
        """
        Creates a table in an SQL database

        Parameters
        ----------
        fields : dict
            Fields to create in the table

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

        print(f"Creating the '{self.table}' table...")

        # Build a valid SQL 'CREATE TABLE' command
        sql_string = f'CREATE TABLE {self.table} ('
        for field in fields:
            sql_string += field + ' ' + fields[field] + ','
        sql_string = sql_string.rstrip(',') + ')'

        # Attempt to connect to the SQL server
        try:
            self.cursor.execute(sql_string)

        # If there's a problem, print errors and quit
        except pyodbc.ProgrammingError as e:
            if '42S01' in str(e):
                print(f"The '{self.table}' table already exists")
            else:
                print(
                    (f"Programming error: {e}. "
                     "Check that there are no typos in the SQL syntax")
                )
            return False

        except Exception as e:
            print(f"SQL execution error: {e}")
            return False

        # Commit the SQL changes
        try:
            self.conn.commit()

        # Handle errors
        except Exception as e:
            print(f"SQL commit error: {e}")
            return False

        return True

    def add(self, fields):
        """Add an entry to the database

        Parameters
        ----------
        fields : dict
            A dictionary that includes named fields and values to write

        Raises
        ------
        Exception
            If there were errors writing to the database

        Returns
        -------
        True : boolean
            If the write was successful
        False : boolean
            If the write failed
        """

        # We need columns and values
        #   Both are strings, a comma separates each entry
        # Create empty strings for columns and corresponding values
        columns = ''
        values = ''

        # Populate the columns and values (comma after each entry)
        for field in fields:
            columns += field + ', '
            values += f"\'{str(fields[field])}\', "

        # Clean up the trailing comma, to make this valid
        columns = columns.strip(", ")
        values = values.strip(", ")

        # Build the SQL command as a string
        sql_string = f'INSERT INTO {self.table} ('
        sql_string += columns
        sql_string += ')'

        sql_string += '\nVALUES '
        sql_string += f'({values});'

        # Try to execute the SQL command (add rows)
        try:
            self.cursor.execute(sql_string)

        except Exception as err:
            if 'Violation of PRIMARY KEY constraint' in str(err):
                print("Error: This primary key already exists")
            else:
                print(f"SQL execution error: {err}")
                print(f"attempted to write:\n{fields}")
            return False

        # Commit the transaction
        try:
            self.conn.commit()
        except Exception as err:
            print(f"SQL commit error: {err}")
            return False

        # If all was good, return True
        return True

    def read(self, field, value):
        """Read an entry from the database

        Parameters
        ----------
        field : str
            The field to look in (usually an ID)
        value : str
            The value to look for (perhaps a UUID)

        Raises
        ------
        Exception
            If there were errors reading from the database

        Returns
        -------
        entry : str
            The entry, it it was found
        None :
            If there was no match
        False : boolean
            If the read failed
        """

        # Build the SQL string
        sql_string = "SELECT *\n"
        sql_string += f"FROM [{self.db}].[dbo].[{self.table}]\n"
        sql_string += f"\nWHERE {field} = \'{value}\';"

        # Send the SQL command to the server and execute
        entry = None
        try:
            self.cursor.execute(sql_string)
            for row in self.cursor:
                entry = row

        # If there was a problem reading
        except Exception as err:
            if '42S02' in str(err):
                print("Invalid object")
                print("Check the table name is correct")
            else:
                print(f"SQL read error: {err}")
            return False

        # If it all worked, return the entry
        return entry

    def update(self, field, value, body):
        """Update an entry in the database

        Parameters
        ----------
        field : str
            The field to look in (usually an ID)
        value : str
            The value to look for (usually a UUID)
        body : dict
            Values to update

        Raises
        ------
        Exception
            If there were errors reading from the database

        Returns
        -------
        entry : str
            The entry, it it was found
        None :
            If there was no match
        False : boolean
            If the read failed
        """

        # Build the UPDATE command
        sql_string = f"UPDATE [{self.db}].[dbo].[{self.table}]\n"

        # Build the SET command
        sql_string += "SET "
        for entry in body:
            sql_string += f"{entry} = \'{body[entry]}\', "

        # Clean up the SET command
        sql_string = sql_string.strip(", ")
        sql_string += '\n'

        # Build the WHERE command
        sql_string += f"WHERE {field} = \'{value}\';"

        # Try updating the entry
        try:
            self.cursor.execute(sql_string)

        # If there was a problem updating
        except Exception as err:
            print(f"SQL read error: {err}")
            return False

        # Commit the transaction
        try:
            self.conn.commit()
        except Exception as err:
            print(f"SQL commit error: {err}")
            return False

        # If it all worked
        return True

    def delete(self, field, value):
        """Delete an entry from the database

        Parameters
        ----------
        field : str
            The field to search by
        value : str
            The value in the field to find

        Raises
        ------
        Exception
            If there were errors deleting from the database

        Returns
        -------
        True : boolean
            If the write was successful
        False : boolean
            If the write failed
        """

        # Build the SQL string
        sql_string = f'DELETE FROM {self.table}\n'
        sql_string += f'WHERE {field} = \'{value}\';'

        # Try to execute the SQL command (add rows)
        try:
            self.cursor.execute(sql_string)

        except Exception as err:
            print(f"SQL execution error: {err}")
            return False

        # Commit the transaction
        try:
            self.conn.commit()

        except Exception as err:
            print(f"SQL commit error: {err}")
            return False

        # If all was good, return True
        return True


'''
To Do
Update multiple columns at once
Handle integers (currently escaping quotes makes this all strings)
'''
