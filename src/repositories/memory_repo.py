import heapq
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
        
    def get_memories_by_keyword(self, keyword: str) -> list[Memory]:
        return (
            self.session.query(Memory)
            .join(Memory.keywords)
            .filter(Keyword.word == keyword)
            .all()
        )
    
    def get_memories_by_keywords(self, keywords: list[str], k: int) -> list[Memory]:
        memories: list[Memory] = []
        for word in keywords:
            mems = self.get_memories_by_keyword(word)
            memories.extend(mems)
        
        scored_memories = []
        for memory in set(memories):
            score = sum(1 for kw in memory.keywords if kw.word in keywords)
            scored_memories.append((score, memory))
        
        scored_memories = sorted(
            scored_memories,
            key=lambda x: x[0],
            reverse=True
        )

        k = max(k, 1)
        top_k = []
        previous_score = 0
        for idx, memory in enumerate(scored_memories):
            top_k.append(memory[1])
            previous_score = memory[0]

            if memory[0] == previous_score:
                continue

            if idx >= k - 1:
                break

        return top_k
    

