from pydantic import BaseModel, Field
from typing import List
from collections import OrderedDict

# Data model for Grader LLM output format
class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""
    binary_score: str = Field(
        description="Documents are relevant to the question, 'yes' or 'no'"
    )
    
# Function to filter deduplicate documents based on their content
def deduplicate_documents_by_content(docs: List) -> List:
    seen = OrderedDict()
    for doc in docs:
        content_key = doc.page_content.strip()
        if content_key not in seen:
            seen[content_key] = doc
    return list(seen.values())