"""
Creates the table in the database for devices

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
TABLE_NAME = 'devices'
FIELDS = {
    'id': 'uniqueidentifier PRIMARY KEY not null',
    'name': 'varchar(32) not null',
    'site': 'uniqueidentifier not null',
    'vendor': 'varchar(16) not null',
    'type': 'varchar(16) not null',
    'auth_type': 'varchar(8) not null',
    'username': 'varchar(48) null',
    'secret': 'varchar(128) null',
    'salt': 'varchar(24) null',
    'token': 'varchar(max) null'
}


# Create the tables
if __name__ == '__main__':
    # Connect to the DB
    print("Connecting to the database...")

    with SqlServer(server=SQL_SERVER, db=DATABASE, table=TABLE_NAME) as my_sql:
        # Create tables
        my_sql.create_table(fields=FIELDS)
