from pydantic import BaseModel, Field


class CreateToken(BaseModel):
    sub: str = Field(..., max_length=50)

class Token(CreateToken):
    exp: int #unix timestamp (int)