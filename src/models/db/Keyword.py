from database import DBBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from .associations import memory_keyword_assoc
from .Memory import Memory

class Keyword(DBBase):
    __tablename__ = "keywords"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    word: Mapped[str] = mapped_column(unique=True)
    
    memories: Mapped[List["Memory"]] = relationship(
        secondary=memory_keyword_assoc, 
        back_populates="keywords"
    )