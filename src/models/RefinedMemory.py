from pydantic import BaseModel, Field
from typing import List

class RefinedMemory(BaseModel):
    """
    Process the user's note. Extract metadata FIRST, then finalize the memory text.
    """
    reasonig: str = Field(
        description="A short sentence identifying the specific names, dates, or entities found. Ex: 'Found names: Angela, Monday.'",
    )
    nametags: List[str] = Field(
        description="Extract ALL Proper Nouns, Dates (e.g. 'Friday'), and Business Terms (e.g. 'Q3'). Return [] if none.",
    )
    keywords: List[str] = Field(
        description="Generate 3-5 lowercase search terms or synonyms. CANNOT BE EMPTY."
    )
    memory: str = Field(
        description="The corrected version of the user's note. Fix grammar/spelling. Keep 'I' perspective."
    )