from openai import OpenAI
from app.services.constants import const
import time
import json
import sqlparse
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML
from app.services.app_db import AppDB
from app.services.db_schema import UserDB

class Txt2SQLEngine():
    
    def __init__(self):
        self.client = OpenAI(
            organization=const.organization,
            project=const.project,
            api_key=const.api_key
        )
        
        txt2sql_assistant_id = const.txt2sql_assistant_id
        self.txt2sql_assistant = self.client.beta.assistants.retrieve(txt2sql_assistant_id)
        
        sql2txt_assistant_id = const.sql2txt_assistant_id
        self.sql2txt_assistant = self.client.beta.assistants.retrieve(sql2txt_assistant_id)
        
        self.app_db=AppDB()
        
        

    def txt2sql(self,user,user_prompt,thread_id = None):
        #getting thread for user 
        if thread_id is None:
            # Create a new thread for the user
            thread = self.client.beta.threads.create()
            # Save the thread with user association
            self.app_db.save_thread_for_user(user[0],str(thread.id), str(self.txt2sql_assistant.id), user_prompt[:10])
            thread_id=thread.id
        db_schema_json=self.app_db.get_user_db(user[8])
        db_schema_json=db_schema_json[2]
        message = self.client.beta.threads.messages.create(
                    thread_id=thread_id,
                    role="user",
                    content=user_prompt
                    )
        
        run = self.client.beta.threads.runs.create_and_poll(
                    thread_id=thread_id,
                    assistant_id=self.txt2sql_assistant.id,
                    instructions=f"""
                    You are an Expert Database administrator with experience in writing complex SQL queries. You will be given a database schema {db_schema_json} in JSON format and a query submitted by the user in natural language. 
                    
                    On the basis of the provided DB_schema (input1) {db_schema_json} and query in natural language (input2), you need to provide 
                    (A) syntactically correct SQL query that can be run on the provide DB_schema to retrieve the expected result,
                    (B) give  the natural language explanation of the SQL query generated and 
                    (C) list of tables used in the SQL query that you provided.
                    YOU DO NOT GIVE ANY OTHER WORDS APART FROM A, B AND C MENTIONED ABOVE

                    If the user asks anything else apart from a query in Natural Language you should reply the exact text 'NOT A VALID QUERY'.

                    You will always return a json with the keys "query", "tables" "explanation"
                    # Steps 

                    1. Parse the DB_schema from their respective inputs.
                    2. Analyse the natural language user query to determine if it involves DB tables.
                    3. If the user query does not involve DB tables, reply the exact text "NOT A VALID QUERY" and provide the reason of why its not a valid
                    4. If the user asks for a correct query,  Formulate the SQL query on the basis of DB_schema.
                    5. List the tables used in the formulated query.
                    6. provide the query and explanation in a json
                    # Output Format
                    - provide a json with 3 keys: query, tables and explanation
                    - Provide a syntactically correct SQL query in the query key and query should be on the basis of the provided schema. We should not get errors like "no such column: student_name"
                    - Provide the list of tables occurring in SQL query in the tables key
                    - Output the explanation of the query in the explanation key
                    - in case of "NOT A VALID QUERY" output query key as '' and explanation as why its not a valid query

                    # Examples

                    EXAMPLE 1:
                    - DB_schema (input1): {db_schema_json}
                    - Query in natural language (input2): "Get the highest issued books"

                    - Output in json: 
                    "query":" SELECT * FROM books ORDER BY issue_count DESC LIMIT 1",
                    "tables":["books"],
                    "explanation":"To get the highest issued books we need to check data from the books table and issue_count table."

                    EXAMPLE 2:
                    - DB_schema (input1): {db_schema_json}
                    - Query in natural language (input2): "Get the highest paid employee"
                    - Output in json: 
                    "query":"", "tables":[],
                    "explanation":"Not a valid query because the DB does not contain employee information"

                    EXAMPLE3:
                    - DB_schema (input1): {db_schema_json}
                    - Query in natural language (input2): "What is your name?"
                    - Output in json: 
                    "query":"", "tables":[],
                    "explanation":"NOT A VALID QUERY"
                    
                    EXAMPLE4:
                    - DB_schema (input1): {db_schema_json}
                    - Query in natural language (input2): "which student is the healthiest student?"                   
                    "query": "",
                    "tables": [],
                    "explanation": "NOT A VALID QUERY because The database schema does not contain information about student health or related metrics."
                    
                    EXAMPLE5:
                    - DB_schema (input1): {db_schema_json}
                    - Query in natural language (input2): "which student got rank 2 in 3rd semester?"                   
                    "query": "",
                    "tables": [],
                    "explanation": "NOT A Valid query because The database schema does not contain information about student rankings or semesters."
                    
                    Example of INCORRECT OUTPUT: 
                    DB_schema (input1): {db_schema_json}

                    - Query in natural language (input2): "which student got rank 2 in 3rd semester"
                    - Output:
                     "query": "NOT A VALID QUERY",  "tables": [],   "explanation": "The database schema does not contain information about student rankings or semesters."

                    The above output is incorrect because in case of invalid query, the "query" key should be '' and "explanation" key should have "NOT A VALID QUERY because The database schema does not contain information about student rankings or semesters."

                    Correct output:
                    "query": "",  "tables": [],   "explanation": "NOT A VALID QUERY because The database schema does not contain information about student rankings or semesters."
                    """
                    )
                    
        if run.status == 'completed':
            # Retrieve the latest message only
            response_data = self.client.beta.threads.messages.list(thread_id=thread_id)
    
            # Assuming the response_data is a list of messages, get the last one
            if response_data:
                response_data=list(response_data)
                latest_message = response_data[0]  # Get the last message in the thread
                if latest_message.content and isinstance(latest_message.content, list):
                    for content_block in latest_message.content:
                        # Each content block has a 'text' attribute which contains the 'value'
                        if content_block.text and content_block.text.value:
                            response=json.loads(content_block.text.value)
                    print("response: ",response)
                    return response, thread_id
                else:   
                    print("No content in the latest message.")
                    return None, thread_id
            else:
                print("No messages in the thread.")
                return None, thread_id
        else:
            return None,thread_id
        
    def sql2txt(self,user_prompt,query,result):
        prompt=json.dumps({"prompt":user_prompt,"query":query,"result":result})
        thread_id="thread_FRrnIVOK7OOJQrKh9p3Pp6EK"
        message = self.client.beta.threads.messages.create(
                    thread_id=thread_id,
                    role="user",
                    content=prompt
                    )
        run = self.client.beta.threads.runs.create_and_poll(
                    thread_id=thread_id,
                    assistant_id=self.sql2txt_assistant.id,
                    instructions=f"""
                    You are an Expert Database administrator with experience in writing and decoding complex SQL queries. You will be given an SQL query and the result of the query in JSON format.

                    On the basis of the provided a prompt(input 1), SQL Query(input2) for the prompt and the result of the query (input3), you need to provide a translation  of the result in natural language
                    
                    # Steps 
                    1. Understand the prompt
                    1. Understand the SQL query to see what is being asked from the query and associate it with the prompt asked by the user
                    2. Analyse the provided output result and associate it with the SQL Query
                    3.Provide a natural language translation of the result
                    4. DO NOT say anything else except translating the result into English language
                   

                    # Output Format
                    - provide a string sentence or paragraph with the translation
                    """
                    )
                    
        if run.status == 'completed':
            # Retrieve the latest message only
            response_data = self.client.beta.threads.messages.list(thread_id=thread_id)

            # If response data is available
            if response_data:
                response_data = list(response_data)
                latest_message = response_data[0]  # Get the last message in the thread

                if latest_message.content and isinstance(latest_message.content, list):
                    for content_block in latest_message.content:
                        # Ensure content_block.text exists and contains valid text
                        if hasattr(content_block, 'text') and content_block.text and hasattr(content_block.text, 'value'):
                            text_response = content_block.text.value.strip()  # Get the plain text response

                            if text_response:  
                                print("Response: ", text_response)
                                return text_response
                            else:
                                print("Received empty response.")
                                return None
                else:
                    print("No content in the latest message.")
                    return None
            else:
                print("No messages in the thread.")
                return None
        else:
            print("Assistant run did not complete successfully.")
            return None
        
        
    def run_query_on_user_db(self,user,query):
        connection_url=self.app_db.get_user_db_connection(user[0])
        user_db=UserDB()
        result=user_db.get_data_from_db(connection_url[0],query)
        formatted_result = "\n".join([str(row) for row in result])
        return formatted_result
        
    def check_permissions(self,user,query,tables):
        parsed = sqlparse.parse(query)
        statement = parsed[0]  # Assuming a single statement
        # Traverse tokens
        query_type=statement.tokens[0].ttype
        dml_query_type=statement.get_type().upper() 
        print(dml_query_type)
        allowed=False
        policy=json.loads(self.app_db.get_user_permissions(user[0])[0])
        #query_dtls=self.extract_query_details(query)
        print("POLICY: ",policy)
        print("QUERY_DTLS: ",tables)
        print("QUERY TYPE:",query_type)
        if query_type is DML:  
            if dml_query_type=='SELECT': 
                if tables!=[] and all(item in policy['read'] for item in tables):
                    allowed=True
                    msg=query
                else:
                    msg="Access denied to this data"
            else:
                msg="Only SELECT is allowed"      
        else:   
            msg="Only DML is allowed"
      
        return {"allowed":allowed,"msg":msg}
        
        
    '''
    def extract_query_details(self,sql_query):
        parsed = sqlparse.parse(sql_query)
        statement = parsed[0]  # Assuming a single statement
        query_dtls = {"type": None, "tables": []}
        tables = []
        # Traverse tokens
        query_dtls["type"]=statement.tokens[0].ttype
        
        for token in statement.tokens:
            if token.ttype is Keyword and token.value.upper() in {"FROM", "JOIN"}:
                # Get the next token after FROM/JOIN
                next_token = statement.token_next(statement.token_index(token))[1]

                if isinstance(next_token, Identifier):
                    # Single table
                    tables.append(next_token.get_real_name())
                elif isinstance(next_token, IdentifierList):
                    # Multiple tables
                    for identifier in next_token.get_identifiers():
                        tables.append(identifier.get_real_name())
        
        query_dtls["tables"] = tables
        return query_dtls 
    '''    
    
    def txt2sql_engine(self,user,user_prompt,thread_id):
        if thread_id=='None':
            thread_id=None
        response,thread_id=self.txt2sql(user,user_prompt,thread_id)
        sql_query=response.get('query',None)
        sql_tables=response.get('tables',None)
        sql_query = " ".join(sql_query.split())
        explanation=response.get('explanation',None)
        
        if sql_query != '':
            permissions=self.check_permissions(user,sql_query,sql_tables)
            if permissions['allowed']:
                response=self.run_query_on_user_db(user,permissions['msg'])
                print("RESPONSE:",response)
                result=self.sql2txt(user_prompt,sql_query,response)
                messages = self.client.beta.threads.messages.list(thread_id=thread_id)
                # Find the last assistant message
                last_bot_message = next((msg for msg in messages.data if msg.role == "assistant"), None)
                if last_bot_message:
                    # Extract text content from the message
                    if last_bot_message:
                        last_bot_text = ""
                        if isinstance(last_bot_message.content, list):
                                    for item in last_bot_message.content:
                                        if hasattr(item, 'text') and hasattr(item.text, 'value'):
                                            last_bot_text = item.text.value  # Extract JSON string
                                            break  # Assuming we only need the first text block

                        print("Last Bot Text Extracted:", last_bot_text)
                    bot_message_json = json.loads(last_bot_text)  # Convert to dict
                    bot_message_json['result'] = result  # Append new response
                    updated_content = json.dumps(bot_message_json, indent=4)  # Convert back to JSON string
                                        # Delete the old message (if API supports message deletion)
                    print("updated_content:",updated_content)
                    self.client.beta.threads.messages.delete(thread_id=thread_id, message_id=last_bot_message.id)

                    # Add updated message with appended text
                    self.client.beta.threads.messages.create(
                        thread_id=thread_id,
                        role="assistant",
                        content=[{"type": "text", "text": updated_content}]
                    )
                    
                response={"query":sql_query,"result":result, "response": response}
                print(response)
            else:
                response={"query":sql_query,"msg":permissions['msg'],"result":explanation}
            
            result={'success':True,'message':explanation,'data':[response]} 
        else:
            response={"result":explanation}
            result={'success':False,'message':explanation,'data':[response]} 
        return result
    
    def get_table_columns(self, user, table_name):
        """
        Returns the list of columns for a given table in the user's database schema.
        """
        db_schema_json = self.app_db.get_user_db(user[8])
        if not db_schema_json or len(db_schema_json) < 3:
            return []
        schema = db_schema_json[2]
        if isinstance(schema, str):
            try:
                schema = json.loads(schema)
            except Exception:
                return []
        for table in schema.get("tables", []):
            if table.get("name") == table_name:
                return [col.get("name") for col in table.get("columns", [])]
        return []