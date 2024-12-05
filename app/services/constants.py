import os
class Constants:
    db_url= "sqlite:///../../app_db.db"
    organization='<your org openai id >'
    project='<your openai project id>'
    api_key='<your openai api key>'
    txt2sql_assistant_id="<your openai api key>"
    sql2txt_assistant_id="<your openai api key>"
    app_secret=os.getenv('APP_SECRET', 'b840841ab65d5a17c9efaa6b8e355747cda66f89c06ea2c7c2ed303e09644be7')
    
const=Constants
