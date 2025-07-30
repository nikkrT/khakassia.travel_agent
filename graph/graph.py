from langgraph.graph import StateGraph, END , START
from the_state.agentstate import AgentState
from nodes.nochleg_json import extract_nochleg
from nodes.holiday_json import holiday_extract
from nodes.nature_json import nature_extract
from nodes.turism_type import the_type
from nodes.chat import chat
from nodes.holiday import holiday_type
from nodes.nature_type import nature_type
from tools.router import router


def graph_func():
    builder = StateGraph(AgentState)

    builder.add_node("the_type", the_type)# Вызываем функцию, чтобы получить скомпилированный сабграф
    builder.add_node("nochleg_extract", extract_nochleg)
    builder.add_node("holiday_extract", holiday_extract)
    builder.add_node("nature_extract", nature_extract)
    builder.add_node('chat',chat)
    builder.add_node('holiday_type',holiday_type)
    builder.add_node('nature_type',nature_type)

    # 2. Устанавливаем точку входа



    builder.add_conditional_edges(START, router,
                                  {
                                      "the_type": 'the_type',
                                      "holiday_type" : 'holiday_type',
                                      'nature_type':'nature_type',
                                      "END" : END
                                  }
                                  )
    builder.add_conditional_edges(
        "the_type",  # Исходный узел
        lambda s: s['route'],  # Функция, которая определяет маршрут
        {
            'chat' : 'chat',
            "nochleg_extract": "nochleg_extract",
            'holiday_type': 'holiday_type'
        }
    )

    # Добавляем ребро от nochleg_extract к концу, если после него ничего нет
    builder.add_edge("nochleg_extract", END)
    builder.add_edge("holiday_extract", END)
    builder.add_conditional_edges('holiday_type',
                                  lambda s: s['route'],
                                  {'holiday_extract': 'holiday_extract',
                                   'chat': 'chat',
                                   "nature_type": 'nature_type'})
    builder.add_conditional_edges('nature_type',
                                  lambda s: s['route'],
                                  {'END': END,
                                   'chat': 'chat',
                                   "nature_extract": 'nature_extract'})
    graph = builder.compile()

    return graph