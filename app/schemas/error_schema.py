from pydantic import BaseModel


class ErrorSchema(BaseModel):
    code: int
    message: str