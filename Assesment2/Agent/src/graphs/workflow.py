from langgraph.graph import StateGraph, START, END

from src.graphs.state import AgentState
from src.graphs.nodes import (
    router_node,
    retrieve_node,
    answer_node,
    calculator_node
)

graph = StateGraph(AgentState)

graph.add_node("router", router_node)
graph.add_node("retrieve", retrieve_node)
graph.add_node("answer", answer_node)
graph.add_node("calculator", calculator_node)

graph.add_edge(START, "router")

graph.add_conditional_edges(
    "router",
    lambda state: state["route"],
    {
        "rag": "retrieve",
        "calculator": "calculator"
    }
)

graph.add_edge("retrieve", "answer")
graph.add_edge("answer", END)
graph.add_edge("calculator", END)

workflow = graph.compile()