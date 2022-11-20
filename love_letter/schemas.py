from typing import List, Optional

from pydantic import BaseModel


class GameBaseSchema(BaseModel):
    id: Optional[int]
    player_name: str
    status: int = 0
    
    def __str__(self):
        return f"Game id: {self.id}, player_name:{self.player_name}, status: {self.status}"
    
    class Config:
        orm_mode = True
