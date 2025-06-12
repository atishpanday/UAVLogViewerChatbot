from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv(".env")

class Model:
    def __init__(self):
        self.openai = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            model=os.getenv("OPENAI_MODEL"),
            temperature=0.5,
        )
    
    def get_llm(self):
        return self.openai
    
model = Model()