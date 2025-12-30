from .Agent import Agent

from langchain.messages import HumanMessage
from models.schemas import RequestCategorization
from prompts import RequestCategorizerPrompt

class RequestCategorizationAgent(Agent):
    def __init__(self, model):
        prompt = RequestCategorizerPrompt("RequestCategorization").get_prompt()
    
        super().__init__(
            model=model,
            system_prompt=prompt,
            response_format=RequestCategorization
        )
    
    def invoke(self, request: str) -> RequestCategorization:
        message = HumanMessage(content=request)
        response = self.agent.invoke({"messages": [message]})
        return response["structured_response"]