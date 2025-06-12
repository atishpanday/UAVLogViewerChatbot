from common.models.message import Message
from langchain_core.messages import HumanMessage, AIMessage

def parse_messages(messages: list[Message]):
    parsed_messages = []
    for message in messages:
        if message.role == 'user':
            parsed_messages.append(HumanMessage(content=message.content))
        else:
            parsed_messages.append(AIMessage(content=message.content))
    return parsed_messages