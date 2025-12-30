from .Agent import Agent

from langchain.messages import HumanMessage
from models.schemas import RefinedMemory
from prompts import MemoryRefinePrompt

class MemoryRefineAgent(Agent):
    def __init__(self, model):
        prompt = MemoryRefinePrompt("RefinedMemory").get_prompt()
        super().__init__(
            model=model,
            system_prompt=prompt,
            response_format=RefinedMemory
        )
    
    def invoke(self, content: str) -> RefinedMemory:
        message = HumanMessage(content=content)
        response = self.agent.invoke({"messages": [message]})
        return response["structured_response"]