from app.services.app_db import AppDB
from fastapi import  HTTPException, status
from app.services.auth_helper import Hash
from app.auth import oauth2

class AuthService:
    def signupOrg(payload: dict):
        try:
            new_user = {
                'email': payload['email'],
                'org_name': payload['org_name'],
                'password': payload['password']
            }
            user = AppDB().create_new_user(new_user)
            access_token = oauth2.create_access_token({'sub': user[0], 'role': user[1]})
            data = {
                'access_token': access_token,
                'token_type': 'Bearer',
                'user_id': user[0],
                'username': 'root'
            }
            return {
                'success': True,
                'message': 'Account create successfully.',
                'data': [data]
            }
        except Exception as e:
            print(str(e))
            return {
                'success': False,
                'message': 'Oops something went wrong.'
            }
        
    def login(payload):
        if payload['email'] is not None:
            user = AppDB().get_user_by_email(payload['email'])
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Credentials')
        if not Hash.verify(user[7], payload["password"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Credentials')
        access_token = oauth2.create_access_token({'sub': user[0], 'user_type': user[9]})
        print(user[0])
        thread_count = AppDB().get_threadcount_for_user(user[0])
        data= {
            'access_token': access_token,
            'token_type': 'Bearer',
            'user_id': user[0],
            'username': user[1],
            'thread_count': thread_count
        }
        return {
                'success': True,
                'message': 'Login Successful',
                'data':[data]
            }
        