from database import DBBase
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from .associations import memory_keyword_assoc
from .Keyword import Keyword

class Memory(DBBase):
    __tablename__ = "memories"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    memory: Mapped[str] = mapped_column()
    
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.now()
    )

    keywords: Mapped[List["Keyword"]] = relationship(
        secondary=memory_keyword_assoc, 
        back_populates="memories"
    )