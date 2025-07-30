from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from promts.nodes_promt import CHAT_PROMPTS
from tools.config import gigachat
from the_state.agentstate import AgentState

def chat(state: AgentState) -> AgentState:
    # Получаем ID промпта из состояния
    prompt_id = state['prompt_id']
    # Находим сам текст системного промпта в словаре
    system_prompt = CHAT_PROMPTS[prompt_id]

    # Создаем шаблон чата с системным промптом
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder('chat_history'),
        ('human', '{input}')
    ])

    # Собираем цепочку
    chat_chain = chat_prompt | gigachat

    # Вызываем цепочку. 'promt_id' здесь не нужен, так как он не является переменной в шаблоне.
    response = chat_chain.invoke({
        'chat_history': state.get('chat_history', []), # Используем .get для безопасности
        "input": state["input"]
    })
    usage=response.usage_metadata['total_tokens']
    response=StrOutputParser().invoke(response)
    state['result'] = response
    with open('usage.txt','a') as f:
        f.write(f'AI: usage: \n{usage}\n')
    print(f"Ответ от LLM: {response}")

    return state