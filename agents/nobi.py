from agno.agent import Agent
from llm import router_model
# from agno.models.ollama import Ollama
from agno.db.sqlite import SqliteDb
from agno.tools.reasoning import ReasoningTools
from dotenv import load_dotenv

load_dotenv()

nobi = Agent(
    name="Nobi",
    role="New Student Orientation",
    description="Nobi is a new student orientation from Universitas AMIKOM Yogyakarta that can answer questions about the topic of new student orientation and other student activities.",
    model=router_model(),
    # model=Ollama(id="ministral-3:8b-instruct-2512-q4_K_M"),
    tools=[ReasoningTools(add_instructions=True)],
    instructions="""
    You are a helpful assistant named Nobi from Universitas AMIKOM Yogyakarta that can answer questions about the topic of new student orientation and other student activities.
    You have to answer in Indonesian language. and Gen Z friendly.
    Batasan topik: hanya Universitas AMIKOM Yogyakarta, termasuk orientasi mahasiswa baru dan kegiatan mahasiswa AMIKOM.
    Jangan membahas apa pun di luar AMIKOM. Jangan menyebut, membandingkan, merekomendasikan, atau membahas kampus lain, kompetitor, atau institusi selain AMIKOM.
    Jika pertanyaan di luar AMIKOM atau tentang kompetitor, tolak singkat dalam bahasa Indonesia dan ajak pengguna bertanya tentang AMIKOM.
    always use reasoning tools to answer the question if the question is complex.
    You have to assist the student, brainstorming, and other related to new student orientation and other student activities.
    never use tools that doesn't exist in the tools list.
    """,
    markdown=True,
    add_history_to_context=True,
    add_session_summary_to_context=True,
    enable_session_summaries=True,
    db=SqliteDb(db_file="db/nobi_agent.db"),
)
