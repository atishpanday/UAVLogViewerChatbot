from pydantic import BaseModel
from common.models.message import Message

class MessageRequest(BaseModel):
    messages: list[Message]