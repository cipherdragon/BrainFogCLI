from .base_repository import BaseRepository
from datetime import datetime
from models.db import Memory, Keyword

class MemoryRepository(BaseRepository):
    def __init__(self, session) -> None:
        super().__init__(session)
    
    def commit(self) -> None:
        self.session.commit()

    def add_memory(self, memory: str, timestamp: datetime) -> Memory:
        new_memory = Memory(memory=memory, timestamp=timestamp)
        self.session.add(new_memory)
        self.session.flush()
        return new_memory
    
    def add_keywords(self, memory: Memory, keywords: list[Keyword]) -> None:
        memory.keywords.extend(keywords)
        
    
    
    

