import json, os,streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from the_state.agentstate import AgentState
from tools.config import gigachat
from promts.nodes_promt import CHOICE_CLASS_PROMPT_HOLIDAY,CHOICE_PROMPT

# --- 1. Конфигурация ---
JSON_FILE_PATH = "data/vidy-otdiha.json" # Путь к вашему файлу с категориями


router_prompt_template = ChatPromptTemplate.from_messages([
    ("system", CHOICE_CLASS_PROMPT_HOLIDAY),
    ("human", "Запрос пользователя: {user_query}")
])


router_chain = router_prompt_template | gigachat | StrOutputParser()


# Цепочка №2: Составитель рекомендаций
# Эта цепочка получает отфильтрованные данные и составляет красивый ответ.
recommender_prompt_template = ChatPromptTemplate.from_messages([
    ("system", CHOICE_PROMPT)
])

recommender_chain = recommender_prompt_template | gigachat

def holiday_extract(state: AgentState):
    print("--- Запущен узел рекомендаций по категориям ---")
    user_query = state["input"]
    # ШАГ 1: Определяем категорию с помощью роутера
    print(f"Определяю категорию для запроса: '{user_query}'")
    try:
        # Загружаем список всех категорий из файла
        with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
            all_categories = list(json.load(f).keys())
            print(all_categories)


        chosen_category = router_chain.invoke({
            "user_query": user_query
        })
        print(f"-> Выбрана категория: '{chosen_category}'")
        chosen_category=(chosen_category)

    except Exception as e:
        print(f"Ошибка при выборе категории: {e}.")
        state[
            "result"] = "К сожалению, у меня возникли технические проблемы с доступом к базе данных видов отдыха. Попробуйте позже."
        return state

    # ШАГ 2: Читаем данные только из выбранной категории
    try:
        with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
            all_data = json.load(f)
            relevant_items = all_data.get(chosen_category, [])
            print(f"Загружено {len(relevant_items)} объектов из категории '{chosen_category}'")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Критическая ошибка: не удалось загрузить файл {JSON_FILE_PATH}. {e}")
        state[
            "result"] = "К сожалению, у меня возникли технические проблемы с доступом к базе данных видов отдыха. Попробуйте позже."
        return state

    # ШАГ 3: Генерируем финальную рекомендацию
    if not relevant_items:
        state[
            "result"] = f"К сожалению, по вашему запросу в категории '{chosen_category}' ничего не найдено. Может, попробуем что-то другое?"
        return state

    print("Генерирую финальный ответ...")
    final_response = recommender_chain.invoke({
        "user_query": user_query,
        "context": json.dumps(relevant_items, ensure_ascii=False, indent=2)
    })

    # final_response='тут результаты поиска'
    usage = final_response.usage_metadata['total_tokens']
    with open('usage.txt', 'a', encoding='utf-8') as f:
        f.write(f'holiday json extraction usage: {usage}\n')
    final_response = StrOutputParser().invoke(final_response)
    params = st.session_state.params_flow
    params['holiday_recommendation']=True
    state["result"] = final_response


    print("--- Узел рекомендаций завершил работу ---")
    return state