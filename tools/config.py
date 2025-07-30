import os
from dotenv import load_dotenv
load_dotenv()
from langchain_gigachat import GigaChat

MAX_URLS = 5

SEED = 0
TEMPERATURE = 0.1
TOP_P = 1.0


OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")

gigachat=GigaChat(
    credentials=OPEN_ROUTER_API_KEY,
    model="GigaChat-2-Max",
    temperature=TEMPERATURE,
    top_p=TOP_P,
    streaming=True,
    verify_ssl_certs=False
)