from pydantic import BaseModel
from typing import List

class Candidate(BaseModel):
    name: str
    contact: dict
    skills: List[str]
    experience: List[str]
    education: List[str]
    score: float