from typing import TypedDict, Union
from langgraph.graph import StateGraph, END, START

class AgentState(TypedDict): 
    first_number: Union[float, int]
    second_number: Union[float, int]
    third_number: Union[float, int]
    fourth_number: Union[float, int]
    first_result: Union[float, int]
    second_result: Union[float, int]
    first_operation: str
    second_operation: str


# the nodes of the graph 

def first_adder(state: AgentState) -> AgentState: 
    state["first_result"] = state["first_number"] + state['second_number']
    return state

def second_adder(state: AgentState) -> AgentState: 
    state["second_result"] = state["third_number"] + state["fourth_number"]
    return state

def first_subtractor(state: AgentState) -> AgentState: 
    state["first_result"] = state["first_number"] - state["second_number"]
    return state

def second_subtractor(state: AgentState) -> AgentState: 
    state['second_result'] = state['third_number'] - state['fourth_number']
    return state

# conditional nodes 
def first_router(state: AgentState): 
    if state["first_operation"] == "+": 
        return "first_adder"
    elif state["first_operation"] == "-": 
        return "first_subtractor"


def second_router(state: AgentState): 
    if state["second_operation"] == "+": 
        return "second_adder"
    elif state["second_operation"] == "-": 
        return "second_subtractor"


graph = StateGraph(AgentState)

graph.add_node("first_adder", first_adder)
graph.add_node("second_adder", second_adder)
graph.add_node("first_subtractor", first_subtractor)
graph.add_node("second_subtractor", second_subtractor)

graph.add_node("first_router", lambda state: state)
graph.add_node("second_router", lambda state: state)

graph.add_edge(START, "first_router")
graph.add_conditional_edges(
    "first_router", 
    first_router, 
    {
        "first_adder": "first_adder", 
        "first_subtractor": "first_subtractor"
    }
)

graph.add_edge("first_adder", "second_router")
graph.add_edge("first_subtractor", "second_router")

graph.add_conditional_edges(
    "second_router", 
    second_router, 
    {
        "second_adder": "second_adder", 
        "second_subtractor": "second_subtractor"
    }
)

graph.add_edge("second_subtractor", END)
graph.add_edge("second_adder", END)

app = graph.compile()

problem = AgentState(
    first_number=10, 
    second_number=20, 
    third_number=40, 
    fourth_number=50, 
    first_operation="+", 
    second_operation="-"
)

solution = app.invoke(problem)
print(solution)



