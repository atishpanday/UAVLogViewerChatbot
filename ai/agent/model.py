from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv(".env")

class Model:
    def __init__(self):
        self.googlegenai = ChatGoogleGenerativeAI(
            api_key=os.getenv("GOOGLE_API_KEY"), 
            model=os.getenv("GOOGLE_MODEL"), 
            temperature=0.5,
        )

    def get_googlegenai(self):
        return self.googlegenai
    
model = Model()