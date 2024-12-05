import sqlite3, os
from app.services.constants import const
from app.services.auth_helper import Hash
class AppDB():
    def __init__(self):
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../app_db.db"))
        self.db = sqlite3.connect(db_path) 
        
    
    def get_user_by_email(self,email):
        query = "SELECT * FROM USER WHERE email = ?"
        result = self.db.execute(query, (email,)).fetchone()
        return result if result else None
    
    def get_user_by_id(self,user_id):
        self.db.row_factory = sqlite3.Row 
        query = "SELECT * FROM USER WHERE id = ?"
        result = self.db.execute(query, (user_id,)).fetchone()
        return result if result else None
        
    def create_new_user(self,new_user):
        #add org
        try:
            query = """
                    INSERT INTO org (org_email, org_password, org_name, created_on, updated_on)
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                    RETURNING id;
                    """
            result = self.db.execute(query, (new_user['email'], new_user['password'], new_user['org_name']))
            org_id = result.fetchone()[0]  
            #add new user
            query = """
                    INSERT INTO user (first_name, last_name, date_of_birth, email,phone_number,registration_date,password,org_id,user_type,role_id,created_on, updated_on)
                    VALUES (?,?,?,?,?, CURRENT_TIMESTAMP,?,?,?,?, CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)
                    RETURNING id, role_id;
                    """
            result = self.db.execute(query, ('root','-','-',new_user['email'],'-', new_user['password'],org_id,'admin','root'))
            user = result.fetchone()
            self.db.commit()
            return user
        except Exception as e:
            print(str(e))
            raise e
        
        
    def save_thread_for_user(self, user_id,thread_id, assistant_id,thread_title):
        query = """
                INSERT INTO user_thread (user_id, thread_id, assistant_id, thread_title,created_on, updated_on)
                VALUES (?, ?, ?, ?,CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """
        self.db.execute(query, (user_id, thread_id, assistant_id,thread_title))
        self.db.commit()
    
    def get_thread_for_user(self,user_id):
        self.db.row_factory = sqlite3.Row  
        query = "SELECT thread_id, assistant_id, thread_title FROM user_thread WHERE user_id = ? ORDER BY updated_on DESC"
        result = self.db.execute(query, (user_id,)).fetchall()
        return result if result else None
    
    def get_threadcount_for_user(self,user_id):
        self.db.row_factory = sqlite3.Row  
        query = "SELECT COUNT(*) as thread_count FROM user_thread WHERE user_id = ?"
        result = self.db.execute(query, (user_id,)).fetchone()
        return result['thread_count'] if result else None
   
   
    def get_user_db(self,org_id):
        self.db.row_factory = sqlite3.Row
        query = "SELECT * FROM user_db WHERE org_id=?"
        result = self.db.execute(query, (org_id,)).fetchone()
        return result if result else None
    
    
    def get_user_db_connection(self,user_id):
        query = "SELECT user_db.connection FROM user_db, user WHERE user.org_id= user_db.id and user.id=?"
        result = self.db.execute(query, (user_id,)).fetchone()
        return result if result else None
    
    def get_user_permissions(self,user_id):
        query = "SELECT role.policy FROM role, user WHERE user.role_id= role.id and user.id=?"
        result = self.db.execute(query, (user_id,)).fetchone()
        return result if result else None
    
    def create_user_db(self, connection_string, user_db_json,org_id):
        query = """INSERT INTO user_db (connection, db_schema, org_id,created_on,updated_on)
            VALUES (?,?,?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            RETURNING id;
            """
        result=self.db.execute(query, (connection_string, user_db_json, org_id))
        user_db_id = result.fetchone()[0]  
        self.db.commit()
        return user_db_id
    
    def update_user_db(self,connection_url,user_db_json,org_id):
        query = """UPDATE user_db SET connection = ?, db_schema=?, updated_on = CURRENT_TIMESTAMP WHERE org_id= ? ;"""
        self.db.execute(query, (connection_url,user_db_json,org_id))
        self.db.commit()
        		
    def update_user_db_schema(self,user_db_json,org_id):
        query = """UPDATE user_db SET db_schema=?, updated_on = CURRENT_TIMESTAMP WHERE org_id= ? ;"""
        self.db.execute(query, (user_db_json,org_id))
        self.db.commit()
    
    def create_new_role(self, role_name,role_policy,org_id):
        query = """
                INSERT INTO role (role_name, policy, org_id,created_on, updated_on)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """
        self.db.execute(query, (role_name, role_policy,org_id))
        self.db.commit()
    
    def get_role(self,org_id):
        self.db.row_factory = sqlite3.Row  
        query = "SELECT * FROM role WHERE org_id=?"
        result = self.db.execute(query, (org_id,)).fetchall()
        return result if result else None
    
    def delete_role(self,role_id):
        query = "DELETE FROM role WHERE id=?"
        result = self.db.execute(query, (role_id,))
        self.db.commit()
        
    def add_user(self,user,org_id):
        query = """
                INSERT INTO user (created_on,date_of_birth,email,first_name,last_name,org_id,password,phone_number,registration_date,role_id,updated_on,user_type)
                VALUES (CURRENT_TIMESTAMP,?, ?,?, ?,?,?,?,CURRENT_TIMESTAMP,?,CURRENT_TIMESTAMP,?)
            """
        result=self.db.execute(query, ('22-10-1994', user.email,user.first_name,user.last_name,org_id,Hash.bcrypt(user.password),user.phone_number,int(user.role_id),'user'))
        self.db.commit()
        new_user_id = result.lastrowid
        return new_user_id
    
    def get_user_by_org(self,org_id):
        self.db.row_factory = sqlite3.Row  
        query = "SELECT * FROM user WHERE org_id=? and user_type!='admin'"
        result = self.db.execute(query, (org_id,)).fetchall()
        return result if result else None
    
    def delete_user(self, id):
        query = "DELETE FROM user WHERE id=?"
        result = self.db.execute(query, (id,))
        self.db.commit()
    
    def delete_user_db(self,id):
        query = "DELETE FROM user_db WHERE id=?"
        result = self.db.execute(query, (id,))
        self.db.commit()