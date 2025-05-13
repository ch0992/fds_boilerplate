from pydantic import BaseModel
from typing import List

class AliasEntry(BaseModel):
    alias: str
    description: str

class AliasListResponse(BaseModel):
    aliases: List[AliasEntry]
