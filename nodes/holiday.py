from the_state.agentstate import AgentState
from tools.router import route_decision
import streamlit as st

def holiday_type(state: AgentState):
    state['prompt_id']=1

    response=route_decision({
        'input' : state['input'],
        'chat_history' : state['chat_history']
    },state['prompt_id'],'holiday_type')
    if response == 'nature_type':
        params = st.session_state.params_flow
        params['holiday_recommendation']=False
    state['route']=response

    print(state)
    print(f"Значения в holiday: {state['route']}")

    return state