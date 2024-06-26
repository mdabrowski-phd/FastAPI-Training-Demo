from pydantic import BaseModel


class TaskBody(BaseModel):
    description: str
    priority: int | None = None  # default option
    is_complete: bool = False


class UserBody(BaseModel):
    username: str
    password: str
    is_admin: bool = False
