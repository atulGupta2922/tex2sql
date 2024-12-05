from app.services.app_db import AppDB
from app.services.db_schema import UserDB
import json
class AdminService:
    def create_user_db(self, req, current_user):
        
        try:
            app_db=AppDB()
            org_id=current_user[8]
            user_id=current_user[0]
            if req.db_type == 'mysql':
                connection_string = f"mysql+pymysql://{req.username}:{req.password}@{req.host}:{req.port}/{req.database}"
            elif req.db_type == 'sqlite':
                connection_string = f"sqlite:///{req.file_path}"
            elif req.db_type == 'postgresql':
                connection_string = f"postgresql+psycopg2://{req.username}:{req.password}@{req.host}:{req.port}/{req.database}"
            elif req.db_type == 'mssql':
                connection_string = f"mssql+pyodbc://{req.username}:{req.password}@{req.host}:{req.port}/{req.database}?driver=ODBC+Driver+17+for+SQL+Server"
            else:
                raise ValueError("Unsupported database type")
            print(connection_string)
            if app_db.get_user_db(org_id) is None:
                user_db=UserDB()
                user_db_json=user_db.get_db_schema_as_json(connection_string)
                print(user_db_json)
                user_db_id=app_db.create_user_db(connection_string,user_db_json,org_id)
                user_db=app_db.get_user_db(org_id)
                result={'success':True,'message':'User DB created successfully.','data':user_db}
            else:
                result={'success':False,'message':'User DB already exists.','data':[]}
        except Exception as e:
            result={'success':False,'message':str(e),'data':[]}
        finally:
            return result
        
        
    def update_user_db(self, req, current_user):
        
        try:
            app_db=AppDB()
            org_id=current_user[8]
            user_id=current_user[0]
            if req.db_type == 'mysql':
                connection_string = f"mysql+pymysql://{req.username}:{req.password}@{req.host}:{req.port}/{req.database}"
            elif req.db_type == 'sqlite':
                connection_string = f"sqlite:///{req.file_path}"
            elif req.db_type == 'postgresql':
                connection_string = f"postgresql+psycopg2://{req.username}:{req.password}@{req.host}:{req.port}/{req.database}"
            elif req.db_type == 'mssql':
                connection_string = f"mssql+pyodbc://{req.username}:{req.password}@{req.host}:{req.port}/{req.database}?driver=ODBC+Driver+17+for+SQL+Server"
            else:
                raise ValueError("Unsupported database type")
            print(connection_string)
            if app_db.get_user_db(org_id) is None:
                user_db=UserDB()
                user_db_json=user_db.get_db_schema_as_json(connection_string)
                app_db.update_user_db(connection_string,user_db_json,org_id)
                user_db=app_db.get_user_db(org_id)
                result={'success':True,'message':'User DB created successfully.','data':user_db}
            else:
                result={'success':False,'message':'User DB already exists.','data':[]}
        except Exception as e:
            result={'success':False,'message':str(e),'data':[]}
        finally:
            return result
        
    def get_user_db(self, current_user):
        try:
            app_db=AppDB()
            org_id=current_user[8]
            user_db_data=dict(app_db.get_user_db(org_id))
            result={'success':True,'message':'','data':[user_db_data]}
        except Exception as e:
            result={'success':False,'message':str(e),'data':[]}
        finally:
            return result
        
        
    def refresh_db_schema(self,current_user):
        try:
            app_db=AppDB()
            org_id=current_user[8]
            user_db=UserDB()
            user_db_data=dict(app_db.get_user_db(org_id))
            user_db_json=user_db.get_db_schema_as_json(user_db_data['connection'])
            app_db.update_user_db_schema(user_db_json,org_id)
            user_db=app_db.get_user_db(org_id)    
            result={'success':True,'message':'User DB schema updated successfully.','data':user_db}
        except Exception as e:
            result={'success':False,'message':str(e),'data':[]}
        finally:
            return result
        
    def delete_user_db(self,id,current_user):   
        try:
            app_db=AppDB()
            org_id=current_user[8]
            app_db.delete_user_db(id)
            result={'success':True,'message':'DB deleted successfully','data':[]}
        except Exception as e:
            result={'success':False, 'message':str(e),'data':[]}
        finally:
            return result
        
            
    def create_role(self,role_policy,current_user):
        
        try:
            app_db=AppDB()
            org_id=current_user[8]
            role_name=role_policy['role_name']
           
            result = {"read": [], "write": []}
            
            for table, permissions in role_policy['tables'].items():
                if permissions[0]["read"]:
                    result["read"].append(table)
                if permissions[0]["write"]:
                    result["write"].append(table)
            print("Hello")
            print(result)
            print(str(result))
            print(json.dumps(result))
            app_db.create_new_role(role_name,str(result),org_id)
            # data=app_db.get_role(org_id)
            
            result={'success':True,'message':'Role created successfully','data':[]}
        except Exception as e:
            result={'success':False,'message':str(e),'data':[]}
        finally:
            return result
        
      
    def list_role(self,current_user):
        try:
            app_db=AppDB()
            org_id=current_user[8]
            data=app_db.get_role(org_id)
            result={'success':True,'message':'Role listed successfully','data':data}
        except Exception as e:
            result={'success':False, 'message':str(e),'data':[]}
        finally:
            return result
        
        
    def delete_role(self,id,current_user):
        try:
            app_db=AppDB()
            org_id=current_user[8]
            app_db.delete_role(id)
            data=app_db.get_role(org_id)
            result={'success':True,'message':'Role deleted successfully','data':data}
        except Exception as e:
            result={'success':False, 'message':str(e),'data':[]}
        finally:
            return result
        
        
    '''
    def update_role(self,role_id,current_user):
        try:
            app_db=AppDB()
            org_id=current_user[8]
            data=app_db.update_role(role_id,org_id)
            result={'success':True,'message':'Role created successfully','data':data}
        except Exception as e:
            result={'success':False,'message':str(e),'data':[]}
        finally:
            return result
    '''    

    def create_user(self,request,current_user):
        try:
            app_db=AppDB()
            org_id=current_user[8]
            new_id=app_db.add_user(request,org_id)
            data=app_db.get_user_by_id(new_id)
            result={'success':True,'message':'User created successfully','data':[dict(data)]}
        except Exception as e:
            result={'success':False, 'message':str(e),'data':[]}
        finally:
            return result

    def delete_user(self,id,current_user):
        try:
            app_db=AppDB()
            org_id=current_user[8]
            app_db.delete_user(id)
            result={'success':True,'message':'User deleted successfully','data':[]}
        except Exception as e:
            result={'success':False, 'message':str(e),'data':[]}
        finally:
            return result
    
    def list_user(self,current_user):
        try:
            app_db=AppDB()
            org_id=current_user[8]
            data=app_db.get_user_by_org(org_id)
            result={'success':True,'message':'Users listed successfully','data':data}
        except Exception as e:
            result={'success':False, 'message':str(e),'data':[]}
        finally:
            return result
    
    def add_role(self):
        pass
    
    def update_user(self):
        pass
    
  