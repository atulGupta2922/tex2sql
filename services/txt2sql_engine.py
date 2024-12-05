from openai import OpenAI
import sqlite3
from constants import const


class Txt2SQLEngine():
    
    def __init__(self,user_id):
        self.client = OpenAI(
            organization=const.organization,
            project=const.project,
            api_key=const.api_key
        )
        
        assistant_id = const.assistant_id
        self.assistant = self.client.beta.assistants.retrieve(assistant_id)
        self.db = sqlite3.connect(const.db_url)
        self.schema_json=self.get_user_db_schema(user_id)
        
        
    def save_thread_for_user(self, user_id, thread_id, assistant_id):
        query = """
        INSERT INTO user_thread (user_id, thread_id, assistant_id)
        VALUES (%s, %s, %s)
        ON CONFLICT (user_id) DO UPDATE 
        SET thread_id = EXCLUDED.thread_id, assistant_id = EXCLUDED.assistant_id
        """
        self.db.execute(query, (user_id, thread_id, assistant_id))
        
    
    
    def get_thread_for_user(self,user_id):
         # Query the database for the user's thread
        query = "SELECT thread_id, assistant_id FROM user_thread WHERE user_id = %s"
        result = self.db.execute(query, (user_id,)).fetchone()
        return result if result else None
   
    def get_user_db_schema(self,user_id):
        query = "SELECT user_db.db_schema FROM user_db, user WHERE user.org_id= user_db.org_id and user.user_id=%s"
        result = self.db.execute(query, (user_id,)).fetchone()
        return result if result else None
    
    
    def txt2sql(self,user_prompt,user_id):
        #getting thread for user
        user_thread = self.get_thread_for_user(user_id)
    
        if user_thread is None:
            
            # Create a new thread for the user
            txt2sql_assistant = self.client.beta.assistants.retrieve(self.assistant)
            thread = self.client.beta.threads.create()
            
            
            # Save the thread with user association
            self.save_thread_for_user(user_id, thread.id, txt2sql_assistant.id)
        else:
            # Reuse the existing thread
            thread = user_thread
        
        
        message = self.client.beta.threads.messages.create(
                    thread_id=thread.id,
                    role="user",
                    content=user_prompt
                    )
        run = self.client.beta.threads.runs.create_and_poll(
                    thread_id=thread.id,
                    assistant_id=txt2sql_assistant.id,
                    instructions=f"""
                    You are an Expert Database administrator with experience in writing complex SQL queries.
                    Below is the database schema for reference:
                    {self.schema_json}
                    You need to provide a syntactically correct SQL query that can be run to retrieve the expected result.
                    """
                    )
        
        assistant_response = run["output"]

        # Print the assistant's response
        print("Assistant Response:", assistant_response)

        return assistant_response

        
        