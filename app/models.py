from typing import Optional
from pydantic import BaseModel, Field


class ErrorMessage(BaseModel):
    code: Optional[int] = Field(None, title="Код ошибки")
    message: str = Field(None, title="Текст с описанием ошибки", max_length=4000)
