from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END


class TestState(TypedDict):
    query: str
    final_ans: List[str]


def node(state: TestState):
    ans = [
        "llm model is large language model",
        "slm is small language model"
    ]
    return {"final_ans": ans}


# Graph build
builder = StateGraph(TestState)

# Node add
builder.add_node("test_node", node)

# Edges
builder.add_edge(START, "test_node")
builder.add_edge("test_node", END)

# Compile
research_chatbot= builder.compile()