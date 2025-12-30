from database import DBBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from .associations import memory_keyword_assoc

class Keyword(DBBase):
    __tablename__ = "keywords"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    word: Mapped[str] = mapped_column(unique=True)
    
    memories: Mapped[List["Memory"]] = relationship( # type: ignore
        secondary=memory_keyword_assoc, 
        back_populates="keywords"
    )