from typing import TypedDict, Literal, Optional
from langchain_core.messages import BaseMessage


class CollectedParams(TypedDict):
    accomodation: Optional[bool]
    holiday_recommendation: Optional[bool]
    nature_recommendation: Optional[bool]

class AgentState(TypedDict):
    input: str
    chat_history: list[BaseMessage]
    route: Optional[Literal[
        "the_type",
        "chat",
        "holiday_type",
        "nature_type"
    ]]
    result: Optional[str]
    prompt_id: Optional[int]
    params_flow: CollectedParams
