from datetime import datetime
from models.db.Memory import Memory
from repositories.memory_repo import MemoryRepository
from repositories.keyword_repository import KeywordRepository
from sqlalchemy.orm import Session

def create_memory(session: Session, memory: str,
                  keywords: list[str], timestamp: datetime) -> Memory:
    memory_repo = MemoryRepository(session)
    keyword_repo = KeywordRepository(session)

    keyword_list = keyword_repo.get_or_create_keywords(keywords)
    new_memory = memory_repo.add_memory(memory, timestamp)
    memory_repo.add_keywords(new_memory, keyword_list)
    memory_repo.commit()

    return new_memory