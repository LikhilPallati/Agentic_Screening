from pydantic import BaseModel
from typing import List

# Structure for the response
class Candidate(BaseModel):
    name: str
    contact: dict
    skills: List[str]
    experience: List[str]
    education: List[str]

    score: float
