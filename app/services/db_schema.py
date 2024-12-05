from sqlalchemy import create_engine, inspect, text
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import json, os
import pymysql
import psycopg2
import pyodbc
import sqlite3

class UserDB():
    def __init__(self):
        pass
    
    def check_connection(self,app_db=None,connection_url=None):
        connection_string=connection_url if connection_url is not None else app_db.get_user_db_connection()
        self.engine= create_engine(connection_string)
        try:
            # Check if the database is SQLite and validate the file path
            if self.engine.url.get_backend_name() == "sqlite":
                db_file_path = str(self.engine.url.database)
                if not os.path.exists(db_file_path):
                    raise FileNotFoundError(f"SQLite database file not found at {db_file_path}")

            # Test the connection by executing a lightweight query
            with self.engine.connect() as connection:
                connection.execute(text('SELECT 1'))
                print("Database connection successful.")
            return True
        except Exception as e:
            print(str(e))
            return False

    @staticmethod
    def test_db_connection(req):
        data=[]
        success=True
        message='Connection Test Successful.'
        try:
            if req.db_type == 'mysql':
                connection = pymysql.connect(
                    host=req.host,
                    user=req.username,
                    password=req.password,
                    database=req.database,
                    port=int(req.port),
                    connect_timeout=5
                )
            elif req.db_type == 'sqlite':
                if not os.path.exists(req.file_path):
                    success= False
                    message="SQLite database file not found."
                else:
                    connection = sqlite3.connect(req.file_path)
                
            elif req.db_type == 'postgresql':
                connection = psycopg2.connect(
                    host=req.host,
                    user=req.username,
                    password=req.password,
                    dbname=req.database,
                    port=int(req.port),
                    connect_timeout=5
                )
            elif req.db_type == 'sqlserver':
                connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={req.host},{req.port};DATABASE={req.database};UID={req.username};PWD={req.password}'
                connection = pyodbc.connect(connection_string, timeout=5)
            else:
                message="Unsupported database type"
                success= False
                
        except Exception as e:
            message=f"Connection failed: {e}"
            success= False
        finally:
            return {"success":success,"message":message,"data":data}

    
    def get_data_from_db(self, connection_string,query, params=None):
        engine= create_engine(connection_string)
        with engine.connect() as connection:
            result = connection.execute(text(query),params or {})
        # Fetch all results
        column_names = result.keys()
        # Fetch all the results
        rows = result.fetchall()
        # Combine column names and data into a list of dictionaries
        result_data = [dict(zip(column_names, row)) for row in rows]
        return result_data
    
    
    
    
    def get_db_schema_as_json(self,connection_string):

        engine = create_engine(connection_string)

        try:
            inspector = inspect(engine)
            schema = {}

            for table_name in inspector.get_table_names():
                columns = inspector.get_columns(table_name)
                primary_key = inspector.get_pk_constraint(table_name).get("constrained_columns", [])

                schema[table_name] = {
                    "columns": [
                        {
                            "name": column["name"],
                            "type": str(column["type"]),
                            "nullable": column["nullable"],
                            "default": str(column["default"]) if column["default"] else None,
                        }
                        for column in columns
                    ],
                    "primary_key": primary_key,
                    "foreign_keys": [
                        {
                            "column": fk["constrained_columns"][0],
                            "referred_table": fk["referred_table"],
                            "referred_column": fk["referred_columns"][0],
                        }
                        for fk in inspector.get_foreign_keys(table_name)
                    ],
                }

            return json.dumps(schema, indent=4)

        except Exception as e:
            return json.dumps({"error": str(e)})

        finally:
            engine.dispose()
