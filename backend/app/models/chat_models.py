from pydantic import BaseModel
from typing import List, Dict

class ChatRequest(BaseModel):
    query: str
    chat_history: List[Dict]