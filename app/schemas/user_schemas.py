from pydantic import BaseModel

# Modelos
class User(BaseModel):
    username: str
    email: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class LoginRequest(BaseModel):
    username: str
    password: str