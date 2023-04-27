"""
Creates tables in the database for sites

Run independantly of the main app, to create the table in the database

Modules:
    3rd Party: None
    Custom: sql

Classes:

    None

Functions

    None

Exceptions:

    None

Misc Variables:

    SQL_SERVER : str
        The SQL server name
    DATABASE : str
        The database name
    TABLE_NAME : str
        The table we want to create
    FIELDS : dict
        Fields/type to create in the table

Limitations/Requirements:
    TBA

Author:
    Luke Robertson - April 2023
"""


from sql import SqlServer

SQL_SERVER = 'A-DEV-SQL05'
DATABASE = 'NetworkAssistant_Alerts'
TABLE_NAME = 'sites'
FIELDS = {
    'id': 'uniqueidentifier PRIMARY KEY not null',
    'name': 'varchar(96) not null'
}


# Create the tables
if __name__ == '__main__':
    # Connect to the DB
    print("Connecting to the database...")

    with SqlServer(server=SQL_SERVER, db=DATABASE, table=TABLE_NAME) as my_sql:
        # Create tables
        my_sql.create_table(fields=FIELDS)
