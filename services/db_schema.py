from sqlalchemy import create_engine, inspect
import json



class UserDB():
   
    
    def get_db_schema_as_json(self, connection_string: str):
        # Connect to the database
        engine = create_engine(connection_string)
        inspector = inspect(engine)
        
        # print(inspector.get_table_names())
        # columns = inspector.get_columns('assignments')
        # print(columns)
        # print(inspector.get_pk_constraint('students').get("constrained_columns", []))
        
        # return
        schema = {}
        for table_name in inspector.get_table_names():
            # Fetch columns
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
        
        # Convert to JSON
        return json.dumps(schema, indent=4)

# Example Usage
if __name__ == "__main__":
    db_url = "sqlite:///student_performance.db"
    schema_json = get_db_schema_as_json(db_url)
    print(schema_json)