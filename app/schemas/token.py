from typing import Optional,Union
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class TokenPayload(BaseModel):
    sub: Optional[int] = None
