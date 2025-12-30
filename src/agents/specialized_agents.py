from .Agent import Agent

from models.schemas import RecallQuery, RefinedMemory, RequestCategorization
from prompts import RecallQueryPrompt, MemoryRefinePrompt, RequestCategorizerPrompt

class RequestCategorizationAgent(Agent):
    def __init__(self, model):
        prompt = RequestCategorizerPrompt("RequestCategorization").get_prompt()
    
        super().__init__(
            model=model,
            system_prompt=prompt,
            response_format=RequestCategorization
        )

class RecallQueryAgent(Agent):
    def __init__(self, model):
        prompt = RecallQueryPrompt("RecallQuery").get_prompt()
        super().__init__(
            model=model,
            system_prompt=prompt,
            response_format=RecallQuery
        )

class MemoryRefineAgent(Agent):
    def __init__(self, model):
        prompt = MemoryRefinePrompt("RefinedMemory").get_prompt()
        super().__init__(
            model=model,
            system_prompt=prompt,
            response_format=RefinedMemory
        )