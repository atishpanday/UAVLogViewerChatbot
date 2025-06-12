from fastapi import APIRouter
from agent.agent import agent
from .schema import MessageRequest
from fastapi.responses import StreamingResponse
from common.parse_messages import parse_messages


router = APIRouter(prefix="/chatbot")


@router.post("")
async def chatbot(request: MessageRequest):
    messages = parse_messages(request.messages)
    response = agent.query_analyzer(messages)
    async def stream_response():
        async for chunk in response:
            yield chunk
    return StreamingResponse(stream_response(), media_type="text/event-stream")