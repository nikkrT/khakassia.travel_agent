from the_state.agentstate import AgentState
from tools.router import route_decision
import streamlit as st

def nature_type(state: AgentState) -> AgentState:
    state['prompt_id']=2
    response = route_decision({
        "input": state["input"],
        "chat_history": state["chat_history"]
    },state['prompt_id'],'nature_type')

    print(f'\n\n---{response}---\n\n')
    print(state)
    if response == 'END':
        params=st.session_state.params_flow
        params['nature_recommendation']=False
        state['result']="Рекомендательный цикл окончен. Для повторного рекомендательного цикла нажмите ""Новый диалог"" "
    state['route']=response

    print(f"Значения в nature_type: {state['route']}")

    return state