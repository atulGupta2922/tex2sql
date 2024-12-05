from fastapi import Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class OAuth2PasswordRequestFormCustom(OAuth2PasswordRequestForm):
    def __init__(self, username: Optional[str] = Form(None), email: Optional[EmailStr] = Form(None), password: str = Form(...), scope: str = Form(""), client_id: Optional[str] = Form(None), client_secret: Optional[str] = Form(None)):
        self.email = email
        self.password = password
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret

    async def __call__(self):
        if not self.username and not self.email:
            raise ValueError("Either username or email must be provided.")
        return self