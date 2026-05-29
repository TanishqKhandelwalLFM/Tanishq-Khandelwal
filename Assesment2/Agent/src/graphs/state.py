from typing import TypedDict


class AgentState(TypedDict):
    query: str
    retrieved_docs: list
    answer: str
    tool_result: str
    route: str