from typing import Optional, List

from pydantic import BaseModel, Field


class RepositoryListQuery(BaseModel):
    id: Optional[int] = Field(None, description="id")
    name: Optional[str] = Field(None, description="name")
