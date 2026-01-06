from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
model_name = os.getenv("MODEL") 

class GeminiModel:
    def __init__(self):
        self.api_key = api_key
        self.model = model_name

    def get_llm(self, **kwargs):

        default_kwargs = {
            "temperature": 0.7,
            "max_tokens": 2048,
            "timeout": None,
            "max_retries": 2,
        }
    
        final_kwargs = {**default_kwargs, **kwargs}
        
        return ChatGoogleGenerativeAI(
            model=self.model,
            google_api_key=self.api_key,
            **final_kwargs 
        )