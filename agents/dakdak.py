from agno.agent import Agent
from agno.models.groq import Groq
from agno.models.ollama import Ollama
from agno.db.sqlite import SqliteDb
from agno.vectordb.qdrant import Qdrant
from agno.knowledge.knowledge import Knowledge
from agno.tools.reasoning import ReasoningTools
from dotenv import load_dotenv
import os
# from agno.knowledge.embedder.ollama import OllamaEmbedder

load_dotenv()

# COLLECTION_NAME = "dakdak_collection"
# vector_db = Qdrant(collection=COLLECTION_NAME, url=os.getenv("QDRANT_URL", "http://localhost:6333"), embedder=OllamaEmbedder(id="nomic-embed-text"))
# db = SqliteDb(db_file="db/dakdak_agent.db")

# academic_knowledge = Knowledge(
#     name="academic_knowledge",
#     description="This is a knowledge base that uses a Qdrant Vector DB for academic information",
#     vector_db=vector_db,
#     contents_db=db,
# )

dakdak = Agent(
    name="Dakdak",
    role="Academic Administrator",
    description="Dakdak is a academic administrator from Universitas AMIKOM Yogyakarta that can answer questions about the topic of academic administration.",
    # model=Groq(id="qwen/qwen3-32b", api_key=os.getenv("GROQ_API_KEY_DAKDAK"), temperature=0.6, top_p=0.95),
    model=Ollama(id="ministral-3:8b-instruct-2512-q4_K_M"),
    tools=[ReasoningTools(add_instructions=True)],
    instructions="""
    You are a helpful assistant named Dakdak from Universitas AMIKOM Yogyakarta that can answer questions about the topic of academic administration.
    You have to answer in Indonesian language. and Gen Z friendly.
    always use reasoning tools to answer the question if the question is complex.
    You have a knowledge base named academic_knowledge that can answer questions about the topic of academic administration. You can use this knowledge base to get the information you need.
    You have to assist the student, brainstorming, and other related to academic administration.
    never use tools that doesn't exist in the tools list.
    """,
    markdown=True,
    # db=db,
    # search_knowledge=True,
    add_history_to_context=True,
    add_session_summary_to_context=True,
    enable_session_summaries=True,
    db=SqliteDb(db_file="db/dakdak_agent.db"),
)
