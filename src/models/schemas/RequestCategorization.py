from pydantic import BaseModel, Field
from typing import Literal

class RequestCategorization(BaseModel):
    """
    Classify the user's input into a specific memory operation.
    """
    reasoning: str = Field(
        description="Briefly explain why this input fits the chosen category. Ex: 'User is asking a factual question.'"
    )
    category: Literal["memorize", "recall", "invalid"] = Field(
        description="The strict classification of the request."
    )
    content: str = Field(
        description="The processed content. If 'memorize', clean up grammar. If 'recall', format as a query. If 'invalid', use the fixed canned response."
    )