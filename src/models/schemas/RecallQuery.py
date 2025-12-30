from pydantic import BaseModel, Field
from typing import List

class RecallQuery(BaseModel):
    """
    Structure the user's input for a Vector Database search.
    """
    reasoning: str = Field(
        description="Explain the split between strict filters (names) and semantic topics."
    )
    search_query: str = Field(
        description="The clean, keyword-focused string to be embedded. Remove filler words ('what is', 'do I have')."
    )
    nametag_filters: List[str] = Field(
        default_factory=list,
        description="Extract Proper Nouns (People, Places, Events) from the query to be used as strict metadata filters. Capitalize them."
    )