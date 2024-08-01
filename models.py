from pydantic import BaseModel

class UserMassage(BaseModel):
    user_id: int
    username: str
    text: str
