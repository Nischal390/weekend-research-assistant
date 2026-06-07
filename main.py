import asyncio
import os
from typing import List
from dotenv import load_dotenv
from markitdown import MarkItDown
from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.genai.types import Content, Part

load_dotenv()

# Constants
MODEL_ID = "gemini-2.5-flash"
APP_NAME = "weekend_research_assistant"
USER_ID = "default_user"
SESSION_ID = "research_session"

# Tool for the agent to extract content from URLs or files
def extract_research_content(sources: List[str]) -> str:
    """
    Extracts and converts content from a list of URLs or file paths to Markdown.
    Use this tool whenever the user provides links or files to research.
    """
    md = MarkItDown()
    combined_content = []
    for item in sources:
        try:
            result = md.convert(item)
            combined_content.append(f"--- Source: {item} ---\n{result.text_content}\n")
        except Exception as e:
            combined_content.append(f"Error processing {item}: {e}")
    
    return "\n\n".join(combined_content)

# Define the Research Agent
research_agent = LlmAgent(
    model=MODEL_ID,
    name="WeekendResearchAssistant",
    description="A professional research assistant that can extract content from URLs and files using MarkItDown and synthesize it into comprehensive summaries.",
    instruction=(
        "You are a world-class Research Assistant. Your goal is to help the user synthesize information "
        "from various sources. When the user provides URLs or files, use the 'extract_research_content' tool. "
        "Provide professional, comprehensive summaries and answer follow-up questions based on the extracted content."
    ),
    tools=[PreloadMemoryTool(), extract_research_content]
)

# Setup the runner
runner = InMemoryRunner(agent=research_agent, app_name=APP_NAME)

async def converse():
    # Create a session for the conversation
    await runner.session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )
    
    print("\n--- 🤖 Weekend Research Assistant Agent ---")
    print("I can research URLs and files for you. Type 'exit' to quit.")
    
    while True:
        try:
            # Note: input() might block in some async environments, but for a local script it's fine.
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            
            content = Content(role="user", parts=[Part(text=user_input)])
            
            async for event in runner.run_async(
                user_id=USER_ID,
                session_id=SESSION_ID,
                new_message=content,
            ):
                if event.content and event.content.parts and event.author != "user":
                    for part in event.content.parts:
                        if part.text:
                            print(f"Assistant: {part.text}")
            
            # Save session to memory for context across turns
            session = await runner.session_service.get_session(
                app_name=APP_NAME,
                user_id=USER_ID,
                session_id=SESSION_ID,
            )
            await runner.memory_service.add_session_to_memory(session)
            
        except EOFError:
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(converse())
