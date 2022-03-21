from typing import List
from pydantic import BaseModel
import toml


def load_settings(file_path: str) -> str:
    return "hello"


class Settings(BaseModel):
    mode: str
    users: List[str]
