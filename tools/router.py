import os

from the_state.agentstate import AgentState
from typing import Literal
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from promts.nodes_promt import CHAT_PROMPTS,SYSTEM_ROUTER_PROMPT
from tools.config import gigachat
import streamlit as st


def extract_command(response: str) -> str:
    """
    Извлекает команду 'search' или 'chat' из ответа LLM, даже если ответ содержит дополнительный текст.
    Всегда возвращает одну из двух команд, используя "chat" как безопасное значение по умолчанию.

    Args:
        response: Строка ответа от LLM

    Returns:
        "search" или "chat"
    """
    response = response.strip().lower()

    # Если ответ содержит только "search" или "chat", возвращаем его
    if len(response)<30:
        return response
    print(len(response))

    # Проверяем, начинается ли ответ с "search" или "chat"
    if response.strip().startswith("chat"):
        return "chat"
    if response.strip().startswith("search"):
        return "search"

    # Если не удалось определить команду, возвращаем "chat" как безопасное значение
    print(f"Не удалось определить команду из ответа: '{response}'. Возвращаем 'chat' как безопасное значение.")
    return "chat"

def router(state: AgentState)->Literal["the_type","holiday_type","nature_type","END"]:
    params=st.session_state.params_flow
    print(f'\n\n---{params}---\n\n')
    if params['accomodation'] is None:
        return "the_type"
    elif params['holiday_recommendation'] is None:
        return "holiday_type"
    elif params['nature_recommendation'] is None:
        return 'nature_type'
    else:
        return "END"

def route_decision(value: dict,id,str):
    print("Заходим в route_decision")
    route_prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_ROUTER_PROMPT[id]),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ])

    router_chain = route_prompt | gigachat

    try:
        response = router_chain.invoke(value)
        usage=response.usage_metadata['total_tokens']
        with open('usage.txt', 'a', encoding='utf-8') as f:
            f.write(f'{str} usage: {usage}\n')
        response=StrOutputParser().invoke(response)
        response = extract_command(response)
        print(f"Извлечена команда: {response}")
        return response
    except Exception as e:
        print(f"Ошибка при обработке запроса: {e}")
        return "chat"