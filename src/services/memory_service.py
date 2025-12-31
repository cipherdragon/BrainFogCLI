from datetime import datetime
from langchain_community.vectorstores.faiss import FAISS
from models.db.Memory import Memory
from models.embeddings import GraniteEmbeddings
from repositories.memory_repo import MemoryRepository
from repositories.keyword_repository import KeywordRepository
from sqlalchemy.orm import Session
from config import Config

def create_memory(session: Session, memory: str,
                  keywords: list[str], timestamp: datetime) -> Memory:
    memory_repo = MemoryRepository(session)
    keyword_repo = KeywordRepository(session)

    keyword_list = keyword_repo.get_or_create_keywords(keywords)
    new_memory = memory_repo.add_memory(memory, timestamp)
    memory_repo.add_keywords(new_memory, keyword_list)
    memory_repo.commit()

    return new_memory

def query_memory(session: Session, query: str) -> list[Memory]:
    keyword_repo = KeywordRepository(session)
    all_keywords = [keyword.word for keyword in keyword_repo.get_all_keywords()]
    if not all_keywords:
        return []
    config = Config()
    if config.EMBEDDING_MODEL_PATH is None:
        raise ValueError("EMBEDDING_MODEL_PATH is not set in the configuration.")
    embedding_model = GraniteEmbeddings(model_path=config.EMBEDDING_MODEL_PATH)
    library = FAISS.from_texts(all_keywords, embedding_model)
    results = library.similarity_search(query, k=5)
    keywords = [res.page_content for res in results]
 
    memory_repo = MemoryRepository(session)
    memories = memory_repo.get_memories_by_keywords(keywords, k=3)

    return memories
