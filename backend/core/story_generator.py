import httpx
import uuid
from sqlalchemy.orm import Session
from core.config import Settings
from langchain_core.output_parsers import PydanticOutputParser
import json
from core.prompts import STORY_PROMPT
from models.story import Story,StoryNode
from core.models import StoryLLMResponse, StoryNodelLLM
import uuid
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "fredrezones55/Gemma-4-Uncensored-HauhauCS-Aggressive:e2b" 


class StoryGenerator:
    
    @classmethod
    def _get_llm():
        return MODEL_NAME
    
    @classmethod
    async def generate_story(cls, db:Session, session_id:str,theme:str="fantasy" )->Story:
        parser = PydanticOutputParser(pydantic_object=StoryLLMResponse)
        response = None 
        timeout = httpx.Timeout(connect=10.0, read=300.0, write=30.0, pool=10.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
           format_instructions = parser.get_format_instructions()

           prompt = f"""Generate a short branching story about: {theme}

                {format_instructions}
                
                """
           print(prompt)
           full_text =""
       
           async with client.stream("POST", OLLAMA_URL,                
                    json={
                    "model": MODEL_NAME,
                    "messages": [
                        {"role": "system", "content":STORY_PROMPT}
                        ,{"role": "user", "content":prompt}],
                    "stream": True,
                    "format": "json",  # tells Ollama to constrain output to valid JSON
                }) as response:

           
               async for line in response.aiter_lines():
                 if line:
                    chunk = json.loads(line)
                    full_text += chunk["message"]["content"]
                    print ("prpceessed line")
        print (full_text)
        
        story_structure = parser.parse(full_text)
        story_db = Story(id=str(uuid.uuid4()),  title = story_structure.title, session=session_id)
        db.add(story_db)
        db.flush()
        
        root_node_data = story_structure.rootNode
        if isinstance(root_node_data,dict):
            root_node_data = StoryNodelLLM.model_validate(root_node_data)
        cls._process_story_node(db, story_db.id, root_node_data, is_root=True)
        db.commit()
        return story_db
    
    @classmethod
    
    def _process_story_node(cls, db: Session, story_id: int, node_data: StoryNodelLLM, is_root: bool = False) -> StoryNode:
        node = StoryNode(
            id = str(uuid.uuid4()),
            story_id=story_id,
            content=node_data.content if hasattr(node_data, "content") else node_data["content"],
            is_root=is_root,
            is_ending=node_data.isEnding if hasattr(node_data, "isEnding") else node_data["isEnding"],
            is_winning_ending=node_data.isWinningEnding if hasattr(node_data, "isWinningEnding") else node_data["isWinningEnding"],
            options=[]
        )
        db.add(node)
        db.flush()

        if not node.is_ending and (hasattr(node_data, "options") and node_data.options):
            options_list = []
            for option_data in node_data.options:
                next_node = option_data.nextNode

                if isinstance(next_node, dict):
                    next_node = StoryNodelLLM.model_validate(next_node)

                child_node = cls._process_story_node(db, story_id, next_node, False)

                options_list.append({
                    "text": option_data.text,
                    "node_id": child_node.id
                })

            node.options = options_list

        db.flush()
        return node