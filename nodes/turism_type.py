from the_state.agentstate import AgentState
from tools.router import route_decision
import streamlit as st

def the_type(state: AgentState) -> AgentState:
    state['prompt_id']=0
    response = route_decision({
        "input": state["input"],
        "chat_history": state["chat_history"]
    },state['prompt_id'],'the_type')

    if response == 'holiday_type':
        params=st.session_state.params_flow
        params['accomodation']=False
    state['route']=response

    print(f"Значения в the_type: {state['route']}")

    return state