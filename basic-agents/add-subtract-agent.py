from typing import TypedDict, Union
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict): 
    first_number: Union[int, float]
    second_number: Union[int, float]
    operation: str
    result: str


# define the nodes 
def adder(state: AgentState) -> AgentState: 
    state["result"] = state["first_number"] + state["second_number"]
    return state

def subtractor(state: AgentState) -> AgentState: 
    state["result"] = state["first_number"] - state["second_number"]
    return state

def router(state: AgentState): 
    if state["operation"] == "-": 
        return "subtractor_node"
    elif state["operation"] == "+": 
        return "adder_node"
# build the graph 

graph = StateGraph(AgentState)

graph.add_node("adder_node", adder)
graph.add_node("subtractor_node", subtractor)
graph.add_node("router", lambda state: state)
graph.add_conditional_edges(
    "router", 
    router, 
    {
        "adder_node": "adder_node", 
        "subtractor_node": "subtractor_node"
    }
)

graph.add_edge(START, "router")
graph.add_edge("subtractor_node", END)
graph.add_edge("adder_node", END)

app = graph.compile()

question = AgentState(first_number=33, second_number=2, operation="+")
result = app.invoke(question)
print(result)
