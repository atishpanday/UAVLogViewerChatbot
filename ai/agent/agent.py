from data.vector_store import initialize_vector_store
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from .model import model
from common.models.message import Message
from .schema import QueryType, LogMessageQuery
from data.fetch_logs import fetch_logs
from data.fetch_log_messages import fetch_log_messages
import json
from .prompts import query_analyser_prompt, general_response_prompt, flight_aware_data_fetcher_prompt, flight_aware_response_prompt


class Agent:
    def __init__(self):
        self.llm = model.get_llm()
        self.vector_store, self.index = initialize_vector_store()
    
    def fetch_reference(self, query: str):
        # Search vector store for relevant documents
        docs = self.vector_store.similarity_search(query, k=5)
        
        # Extract and combine the content from retrieved documents
        reference_content = ""
        for doc in docs:
            reference_content += doc.page_content + "\n\n"
            
        return reference_content.strip()
    
    async def query_analyzer(self, messages: list[Message]):
        prompt = ChatPromptTemplate.from_messages([
            ("system", query_analyser_prompt),
            MessagesPlaceholder(variable_name="messages")
        ])
        chain = prompt | self.llm.with_structured_output(QueryType)
        query_type = chain.invoke({ "messages": messages }).query_type

        print(query_type)
        
        if query_type == 'conversation':
            response = self.conversational_response(messages)
        elif query_type == 'general':
            response = self.general_response(messages)
        elif query_type == 'flight':
            response = self.flight_aware_response(messages)
        else:
            raise ValueError(f"Invalid question type: {query_type}")
        
        async for chunk in response:
            yield chunk

    async def conversational_response(self, messages: list[Message]):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant that responds to the user's message with either a general greeting or asks clarifying questions if the user's message is not clear."),
            MessagesPlaceholder(variable_name="messages")
        ])
        chain = prompt | self.llm
        response = chain.astream({"messages": messages})
        
        async for chunk in response:
            yield chunk.content

    async def general_response(self, messages: list[Message]):
        prompt = ChatPromptTemplate.from_messages([
            ("system", general_response_prompt),
            MessagesPlaceholder(variable_name="messages")
        ])
        reference = self.fetch_reference(messages[-1].content)
        chain = prompt | self.llm
        response = chain.astream({"reference": reference, "messages": messages})

        async for chunk in response:
            yield chunk.content

    async def flight_aware_response(self, messages: list[Message]):
        reference = self.fetch_reference(messages[-1].content)
        available_log_messages = json.dumps(await fetch_log_messages())
        prompt = ChatPromptTemplate.from_messages([
            ("system", flight_aware_data_fetcher_prompt),
            MessagesPlaceholder(variable_name="messages")
        ])
        chain = prompt | self.llm.with_structured_output(LogMessageQuery)
        log_message_query = chain.invoke({
            "reference": reference, 
            "available_log_messages": available_log_messages, 
            "messages": messages
        })

        message_types = log_message_query.message_types

        print(message_types)

        logs = []

        for message_type in message_types:
            logs.append(await fetch_logs(message_type.message_type, message_type.metrics))

        logs = json.dumps(logs)

        flight_analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", flight_aware_response_prompt),
            MessagesPlaceholder(variable_name="messages")
        ])
        flight_analysis_chain = flight_analysis_prompt | self.llm
        response = flight_analysis_chain.astream({
            "reference": reference, 
            "logs": logs, 
            "messages": messages
        })
        
        async for chunk in response:
            yield chunk.content


agent = Agent()