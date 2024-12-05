from openai import OpenAI
import sqlite3
from constants import const


class Txt2SQLEngine():
    
    def __init__(self):
        self.client = OpenAI(
            organization='org-0WiJlDAVVOIh4oaisiP49G17',
            project='proj_gWaFdgg8GJTA5FX404f8ooWO',
            api_key='sk-esgate-openai-service-id-dev-bs9EG2Y0QBja7WGt30QbT3BlbkFJImJ2oS36x8cbc90agRj2'
        )
        assistant_id = "asst_nVrytkzJcAMWfho5FkQpl6yL"  # Replace with your assistant's unique ID
        self.assistant = self.client.beta.assistants.retrieve(assistant_id)
        self.db = sqlite3.connect(const.db_path)
        
        
        
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
   

    def txt2sql(self,user_prompt,user_id):
        #getting thread for user
        user_thread = self.get_thread_for_user(user_id)
    
        if user_thread is None:
            
            #fetching db schema
            schema_json = get_db_schema_as_json(db_url)
            
            
            # Create a new thread for the user
            txt2sql_assistant = self.client.beta.assistants.retrieve(self.assistant)
            thread = self.client.beta.threads.create()
            instructions=""
            
            
            
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
                    instructions=""
                    )
        
        
        
        