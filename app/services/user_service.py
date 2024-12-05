from app.services.constants import const
from app.services.app_db import AppDB
from openai import OpenAI


class UserService():
    def __init__(self):
        self.client = OpenAI(
            organization=const.organization,
            project=const.project,
            api_key=const.api_key
        )
        
    def list_thread(self,user):
        result_set = AppDB().get_thread_for_user(user[0])
        if result_set:
            data = [dict(row) for row in result_set]
        else:
            data = []
        print(data)
        result={'success':True,'message': 'Got it','data':  data}
        # rows = data.fetchall()
        # Print rows
        """ for row in rows:
            print(row[0])
            try:
                # Retrieve all messages from the given thread
                messages = self.client.beta.threads.messages.list(thread_id=row[0])
                
                # Format the messages into a readable format
                conversation = []
                for message in messages.data:
                    role = message.role  # "user" or "assistant"
                    content = message.content[0].text.value  # Extract message text
                    conversation.append(f"{role.capitalize()}: {content}")

                # Return formatted conversation
                print("\n".join(conversation))
            
            except Exception as e:
                return f"Error retrieving messages: {str(e)}" """
        return result
    
    def list_chat(self,thread_id):
        try:
            # Retrieve all messages from the given thread
            messages = self.client.beta.threads.messages.list(thread_id=thread_id)
            
            # Format the messages into a readable format
            conversation = []
            user=[]
            assistant=[]
            for message in messages.data:
                role = message.role  # "user" or "assistant"
                content = message.content[0].text.value  # Extract message text
                if role=="user":
                    user.append(content)
                else:
                    assistant.append(content)
                
                conversation.append(f"{role.capitalize()}: {content}")

            # Return formatted conversation
            conversation="\n".join(conversation)
            print("CONVERSATION",conversation)
            return {'success':True,'message': 'Got it','data':  {'user':user,'assistant':assistant}}
        except Exception as e:
            return f"Error retrieving messages: {str(e)}"
        