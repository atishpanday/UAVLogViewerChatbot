from data.vector_store import vector_store
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from .model import model
from common.models.message import Message
from .schema import QueryType, LogMessageQuery
from data.fetch_logs import fetch_logs
from data.fetch_log_messages import fetch_log_messages
import json


class Agent:
    def __init__(self):
        self.googlegenai = model.get_googlegenai()
    
    def fetch_reference(self, query: str):
        # Search vector store for relevant documents
        docs = vector_store.similarity_search(query, k=5)
        
        # Extract and combine the content from retrieved documents
        reference_content = ""
        for doc in docs:
            reference_content += doc.page_content + "\n\n"
            
        return reference_content.strip()
    
    async def query_analyzer(self, messages: list[Message]):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a query analyzer that finds the correct category of the query. Do not answer the query, simply return what type of query it is. For example, if the user asks general questions not specific to a particular flight, return 'general'. If the user asks about a specific flight, return 'flight'. If the user is simply greeting, or you are not sure what the user is asking, return 'conversation'."),
            MessagesPlaceholder(variable_name="messages")
        ])
        chain = prompt | self.googlegenai.with_structured_output(QueryType)
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
        chain = prompt | self.googlegenai
        response = chain.astream({"messages": messages})
        
        async for chunk in response:
            yield chunk.content

    async def general_response(self, messages: list[Message]):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a telemetry expert that can answer knowledge based questions about different log messages of a flight. The question does not refer to any particular flight, but rather general question about telemetry. Answer the question using the context provided here: \n\n {reference}"),
            MessagesPlaceholder(variable_name="messages")
        ])
        reference = self.fetch_reference(messages[-1].content)
        chain = prompt | self.googlegenai
        response = chain.astream({"reference": reference, "messages": messages})

        async for chunk in response:
            yield chunk.content

    async def flight_aware_response(self, messages: list[Message]):
        reference = self.fetch_reference(messages[-1].content)
        available_log_messages = json.dumps(await fetch_log_messages())
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a telemetry expert that can identify the type of log message and metric the user's query is referring to. You need to provide the messageType (the log message) and the list of specific metrics to answer the user's question. ONLY RESPOND WITH ONE OF THE AVAILABLE LOG MESSAGES. Use the context provided here: \n\nREFERENCE MANUAL: \n\n {reference} \n\n The available log messages for the current flight are provided here: \n\nAVAILABLE LOG MESSAGES: \n\n{available_log_messages}"),
            MessagesPlaceholder(variable_name="messages")
        ])
        chain = prompt | self.googlegenai.with_structured_output(LogMessageQuery)
        log_message_query = chain.invoke({
            "reference": reference, 
            "available_log_messages": available_log_messages, 
            "messages": messages
        })

        message_type, metrics = log_message_query.messageType, log_message_query.metrics

        logs = json.dumps(await fetch_logs(message_type, metrics))

        flight_analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a telemetry expert that can analyze the logs of a flight and provide a summary of the logs, answering the user's query. DO NOT MENTION THE DATA THAT YOU USE TO ANSWER THE QUERY. SIMPLY ANSWER THE QUERY. The reference for the logs is provided here: \n\nREFERENCE MANUAL: \n\n{reference} \n\n The logs are provided here: \n\nLOGS: \n\n{logs}"),
            MessagesPlaceholder(variable_name="messages")
        ])
        flight_analysis_chain = flight_analysis_prompt | self.googlegenai
        response = flight_analysis_chain.astream({
            "reference": reference, 
            "logs": logs, 
            "messages": messages
        })
        
        async for chunk in response:
            yield chunk.content


agent = Agent()