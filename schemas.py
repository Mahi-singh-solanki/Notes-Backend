from pydantic import BaseModel

class User(BaseModel):
    name : str
    email : str
    password : str

class Login(BaseModel):
    username : str
    password : str

class Showuser(BaseModel):
    name : str
    email : str
    id:int
    class Config():
        orm_model=True

    

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    
class Summary(BaseModel):
    id: int
    original_text: str
    summary_text: str
    class Config:
        orm_mode = True

class Upload(BaseModel):
    id: int
    text: str
    class Config:
        orm_mode = True

class Note(BaseModel):
    id: int
    notes: str
    class Config:
        orm_mode = True

class Quiz(BaseModel):
    id: int
    quizes: str
    class Config:
        orm_mode = True