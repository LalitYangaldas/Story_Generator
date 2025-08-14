from sqlalchemy.orm import Session

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from db.database import get_db, SessionLocal
from core.prompts import STORY_PROMPT
from models.story import Story, StoryNode  # Assuming StoryNode is defined here
from core.models import StoryLLMResponse, StoryNodeLLM
from core.models import StoryOptionLLM
from dotenv import load_dotenv

load_dotenv()


class StoryGenerator:

    @classmethod
    def _get_llm(cls):
        return ChatOpenAI(model="gpt-3.5-turbo")
    
    @classmethod
    def generate_story(cls, db: Session, session_id: str, theme: str = "fantasy") -> Story:
        llm = cls._get_llm()
        story_parser = PydanticOutputParser(pydantic_object=StoryLLMResponse)

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                STORY_PROMPT
            ),
            (
                "human",
                f"Create the story with this theme: {theme}"
            )
        ]).partial(format_instructions=story_parser.get_format_instructions())

        # Format and invoke the prompt
        formatted_prompt = prompt.invoke({})
        raw_response = llm.invoke(formatted_prompt)

        # Extract content from LLM response
        response_text = raw_response.content if hasattr(raw_response, "content") else str(raw_response)

        # Parse the response into Pydantic model
        story_structure = story_parser.parse(response_text)

        # Save story to DB
        story_db = Story(title=story_structure.title, session_id=session_id)
        db.add(story_db)
        db.flush()  # To get the ID if needed

        # Process root node
        root_node_data = story_structure.rootNode
        if isinstance(root_node_data, dict):
            root_node_data = StoryNodeLLM.model_validate(root_node_data)

        # Process the story tree
        cls._process_story_node(db, story_db.id, root_node_data, is_root=True)

        db.commit()
        return story_db
    
    @classmethod
    def _process_story_node(
        cls,
        db: Session,
        story_id: int,
        node_data: StoryNodeLLM,  # Fixed: was 'node_ StoryNodeLLM'
        is_root: bool = False
    ) -> StoryNode:
        """
        Recursively processes a story node and its options.
        Only accepts StoryNodeLLM objects (or dicts that can be validated into one).
        """
        # Ensure node_data is a StoryNodeLLM instance
        if isinstance(node_data, dict):
            node_data = StoryNodeLLM.model_validate(node_data)

        # Create the database StoryNode
        node = StoryNode(
            story_id=story_id,
            content=node_data.content,
            is_root=is_root,
            is_ending=node_data.isEnding,
            is_winning_ending=node_data.isWinningEnding,
            options=[]  # Will store [{"text": "...", "node_id": 123}, ...]
        )
        db.add(node)
        db.flush()  # Assigns an ID to `node`

        # Process child nodes only if this is not an ending
        if not node.is_ending and node_data.options:
            options_list = []
            for option in node_data.options:
                # Validate the option (contains 'text' and 'nextNode')
                option_data = StoryOptionLLM.model_validate(option)

                # Process the next node (this is a StoryNodeLLM, not an option!)
                next_node_raw = option_data.nextNode
                if isinstance(next_node_raw, dict):
                    next_node_raw = StoryNodeLLM.model_validate(next_node_raw)

                # Recursively create the next node
                child_node = cls._process_story_node(db, story_id, next_node_raw, is_root=False)

                # Link the option text to the generated child node ID
                options_list.append({
                    "text": option_data.text,
                    "node_id": child_node.id
                })

            # Save all options as a list of dicts
            node.options = options_list
            db.flush()

        return node