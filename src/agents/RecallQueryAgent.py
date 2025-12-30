from .Agent import Agent

from langchain.messages import HumanMessage
from models.schemas import RecallQuery
from prompts import RecallQueryPrompt

class RecallQueryAgent(Agent):
    def __init__(self, model):
        prompt = RecallQueryPrompt("RecallQuery").get_prompt()
        super().__init__(
            model=model,
            system_prompt=prompt,
            response_format=RecallQuery
        )
    
    def invoke(self, query: str) -> RecallQuery:
        message = HumanMessage(content=query)
        response = self.agent.invoke({"messages": [message]})
        return response["structured_response"]
