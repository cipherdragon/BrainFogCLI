# src/models/db/associations.py
from sqlalchemy import Table, Column, ForeignKey
from database import DBBase

memory_keyword_assoc = Table(
    "memory_keywords",
    DBBase.metadata,
    Column("memory_id", ForeignKey("memories.id"), primary_key=True),
    Column("keyword_id", ForeignKey("keywords.id"), primary_key=True),
)