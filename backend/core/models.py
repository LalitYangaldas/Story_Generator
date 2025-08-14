from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

# Define StoryOptionLLM
class StoryOptionLLM(BaseModel):
    text: str = Field(description="The text of the option shown to the user")
    nextNode: Dict[str, Any] = Field(description="The text node context and its optional")

# Define StoryNodeLLM
class StoryNodeLLM(BaseModel):
    content: str = Field(description="The main content of the story node")
    isEnding: bool = Field(description="Whether this node is an ending node")
    isWinningEnding: bool = Field(description="Whether this node is a winning node")
    options: Optional[List[StoryOptionLLM]] = Field(default=None, description="The list of options for this node")

# Define StoryLLMResponse
class StoryLLMResponse(BaseModel):
    title: str = Field(description="The title of the story")
    rootNode: StoryNodeLLM = Field(description="The root node of the story")