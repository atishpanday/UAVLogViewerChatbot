from pydantic import BaseModel, Field
from typing import Literal

class QueryType(BaseModel):
    query_type: Literal['general', 'flight', 'conversation']

class LogMessage(BaseModel):
    message_type: str = Field(
        description="The type of log message to be fetched to answer the user's question"
    )
    metrics: list[str] = Field(
        description="The specific metrics to be fetched to answer the user's question"
    )

class LogMessageQuery(BaseModel):
    message_types: list[LogMessage] = Field(
        description="The list of log messages to be fetched to answer the user's question"
    )