from fastapi import FastAPI, Query, Depends, HTTPException, status
# from services.txt2sql_engine import Txt2SQLEngine
from pydantic import BaseModel
from typing import List, Dict, Optional
from app.services.txt2sql_engine import Txt2SQLEngine
from app.services.auth_helper import Hash
from app.services.auth_service import AuthService
from app.auth.OAuth2PasswordRequestFormCustom import OAuth2PasswordRequestFormCustom
from app.auth.oauth2 import get_current_user
from app.services.admin_service import AdminService
from app.services.user_service import UserService
from app.services.db_schema import UserDB
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

origins = [
    'http://localhost',
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/healthcheck")
async def healthcheck():
    """
    Healthcheck route to verify the service is running.
    Returns a JSON response with status.
    """
    return {"status": "ok"}

class Promptrequest(BaseModel):
    prompt: str
    thread_id: str
    
class ApiResponseModel(BaseModel):
    success: bool
    message: str
    data: List

@app.post("/test-assistant", response_model = ApiResponseModel)
async def test_assistant(request: Promptrequest, current_user = Depends(get_current_user)):
    #request = dict(request)
    txt2sql = Txt2SQLEngine()
    result= txt2sql.txt2sql_engine(current_user,request.prompt,request.thread_id)
    return {
            'success': result['success'],
            'message': result['message'],
            'data': result.get('data',[])
        }

class SignUpRequest(BaseModel):
    email: str
    org_name: str
    password: str

@app.post("/signup", response_model = ApiResponseModel)
async def signup(request: SignUpRequest):    
    result=AuthService.signupOrg({
        'email': request.email,
        'org_name': request.org_name,
        'password': Hash.bcrypt(request.password)
    })
    return {
        'success': result['success'],
        'message': result['message'],
        'data': result.get('data',[])
    }

    
@app.post("/login", response_model = ApiResponseModel)
async def login(request: OAuth2PasswordRequestFormCustom = Depends()):
    try:
        result=AuthService.login({
            'email': request.email,
            'password': request.password
        })
        return {
            'success': result['success'],
            'message': result['message'],
            'data': result.get('data',[])
        }
    except HTTPException as e:
        return {
            'success': False,
            'message': e.detail,
            'data': []
        }        

class CreateDbRequest(BaseModel):
    connection_url: str
     
class CreateConnectionRequest(BaseModel):
    db_type:Optional[str] = None
    host:Optional[str] = None
    username:Optional[str] = None
    password:Optional[str] = None
    database:Optional[str] = None
    port:Optional[int] = None
    file_path:Optional[str] = None
    
 
@app.post('/test_connection', response_model = ApiResponseModel)
async def test_db_connection(request: CreateConnectionRequest, current_user = Depends(get_current_user)):
    result = UserDB.test_db_connection(request)
    return {
            'success': result['success'],
            'message': result['message'],
            'data':  result.get('data',[])
        } 
     
@app.post('/user_db', response_model = ApiResponseModel)
async def create_user_db(request: CreateConnectionRequest, current_user = Depends(get_current_user)):
    result = AdminService().create_user_db(request, current_user)
    return {
            'success': result['success'],
            'message': result['message'],
            'data':  result.get('data',[])
        } 

@app.put('/user_db', response_model = ApiResponseModel)
async def update_user_db(request: CreateConnectionRequest, current_user = Depends(get_current_user)):
    result = AdminService().update_user_db(request, current_user)
    return {
            'success': result['success'],
            'message': result['message'],
            'data':  result.get('data',[])
        } 
   
@app.get('/user_db', response_model = ApiResponseModel)
async def update_user_db(current_user = Depends(get_current_user)):
    result = AdminService().get_user_db(current_user)
    return {
            'success': result['success'],
            'message': result['message'],
            'data':  result.get('data',[])
        }  

@app.delete('/user_db/{id}', response_model = ApiResponseModel)
async def delete_user_db(id,current_user = Depends(get_current_user)):
    result = AdminService().delete_user_db(id,current_user)
    return {
            'success': result['success'],
            'message': result['message'],
            'data':  result.get('data',[])
        } 
        
@app.post('/test_connection', response_model = ApiResponseModel)
async def test_db_connection(request: CreateConnectionRequest, current_user = Depends(get_current_user)):
    result = UserDB.test_db_connection(request)
    return {
            'success': result['success'],
            'message': result['message'],
            'data':  result.get('data',[])
        } 

  
@app.get('/refresh_db_schema', response_model = ApiResponseModel)
async def refesh_db_schema(current_user = Depends(get_current_user)):    
    result = AdminService().refresh_db_schema(current_user)
    return {
            'success': result['success'],
            'message': result['message'],
            'data':  result.get('data',[])
        } 
    
    
    
    
class CreateRoleRequest(BaseModel):
    policy: Dict
    
@app.post('/role', response_model = ApiResponseModel) # to create
async def create_role(request: CreateRoleRequest,current_user = Depends(get_current_user)):
    result = AdminService().create_role(request.policy,current_user)
    return {
            'success': result['success'],
            'message': result['message'],
            'data':  result.get('data',[])
        } 
    
@app.get('/role') # to list
async def list_role(current_user = Depends(get_current_user)):
    result = AdminService().list_role(current_user)
    return {
            'success': result['success'],
            'message': result['message'],
            'data':  result.get('data',[])
        } 

@app.put('/role/{id}')


@app.delete('/role/{id}')
async def delete_role(id,current_user = Depends(get_current_user)):
    result = AdminService().delete_role(id,current_user)
    return {
            'success': result['success'],
            'message': result['message'],
            'data':  []
        } 


# @app.get('/user_db/{action}') # to perform list operations on user_db






@app.post("/logout")
async def logout():
    pass 





@app.get("/admin_dashboard")
async def admin_dashboard():
    pass

@app.get("/user_dashboard")
async def user_dashboard(current_user = Depends(get_current_user)):
    pass

@app.get("/listthread")
async def list_thread(current_user= Depends(get_current_user)):
    result = UserService().list_thread(current_user)
    return {
            'success': result['success'],
            'message': result['message'],
            'data':  result.get('data',[])
        } 

@app.post("/listchat/{thread_id}")
async def list_chat(thread_id: str, current_user= Depends(get_current_user)):
    result = UserService().list_chat(thread_id)
    return {
            'success': result['success'],
            'message': result['message'],
            'data':  result.get('data',[])
        } 




class CreateUserRequest(BaseModel):
    # date_of_birth: str
    email: str
    first_name: str
    last_name: str
    password: str
    phone_number: str
    role_id: str
    
@app.post('/user', response_model = ApiResponseModel) # to create
async def create_user(request: CreateUserRequest,current_user = Depends(get_current_user)):
    result = AdminService().create_user(request,current_user)
    return {
            'success': result['success'],
            'message': result['message'],
            'data':  result.get('data',[])
        } 
    
@app.delete('/user/{id}')
async def delete_user(id,current_user = Depends(get_current_user)):
    result = AdminService().delete_user(id,current_user)
    return {
            'success': result['success'],
            'message': result['message'],
            'data':  result.get('data',[])
        } 
@app.get('/user') # to list
async def list_user(current_user = Depends(get_current_user)):
    result = AdminService().list_user(current_user)
    return {
            'success': result['success'],
            'message': result['message'],
            'data':  result.get('data',[])
        } 
    
