import os

from agno.models.openai import OpenAIChat
from dotenv import load_dotenv

load_dotenv()


def router_model():
    return OpenAIChat(
        id=os.getenv("ROUTER_MODEL", "auto"),
        api_key=os.getenv("ROUTER_API_KEY"),
        base_url=os.getenv("ROUTER_BASE_URL", "https://router.fliw.my.id/v1"),
        temperature=0.6,
        top_p=0.95,
    )
