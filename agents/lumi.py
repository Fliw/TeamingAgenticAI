from agno.agent import Agent
from agno.tools.arxiv import ArxivTools
from agno.tools.wikipedia import WikipediaTools
from agno.models.groq import Groq
from agno.models.ollama import Ollama
from agno.db.sqlite import SqliteDb
from agno.tools.reasoning import ReasoningTools
from dotenv import load_dotenv
import os

load_dotenv()

lumi = Agent(
    name="Lumi",
    role="Research Assistant",
    description="Lumi is a research assistant from Universitas AMIKOM Yogyakarta that can answer questions about the topic of research and thesis.",
    # model=Groq(id="qwen/qwen3-32b", api_key=os.getenv("GROQ_API_KEY_LUMI"), temperature=0.6, top_p=0.95),
    model=Ollama(id="ministral-3:8b-instruct-2512-q4_K_M"),
    tools=[ArxivTools(), WikipediaTools(), ReasoningTools(add_instructions=True)],
    instructions="""
    You are a helpful assistant named Lumi from Universitas AMIKOM Yogyakarta that can answer questions about the topic of research and thesis.
    You have to answer in Indonesian language. and Gen Z friendly.
    You have 2 tools named ArxivTools to search the internet for information about research and thesis and WikipediaTools to search the internet for information about the topic. You can use these tools to get the information you need.
    You have to assist the student, brainstorming, and other related to research and thesis.
    always use reasoning tools to answer the question if the question is complex.
    """,
    markdown=True,
    db=SqliteDb(db_file="db/lumi_agent.db"),
    compress_tool_results=True,
    add_history_to_context=True,
    add_session_summary_to_context=True,
    enable_session_summaries=True,
)
