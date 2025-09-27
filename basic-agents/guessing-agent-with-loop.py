from typing import List, TypedDict
from langgraph.graph import StateGraph, START, END
import random

class AgentState(TypedDict): 
    player_name: str
    guesses: List[int]
    attempts: int
    upper_bound: int
    lower_bound: int 

# let's define the nodes 
def generator(state: AgentState) -> AgentState: 
    generated_number = random.randint(state["lower_bound"], state["upper_bound"])
    state["attempts"] += 1
    state["guesses"].append(generated_number)
    print(f"attempt: {state['attempts']}")
    print(f"The generated number at attempt is: {state['guesses'][-1]}")
    return state

def greeter(state: AgentState) -> AgentState: 
    print(f"Hello, {state['player_name']}. \n Wishing you good luck!")
    return state

def hint(state: AgentState) -> AgentState: 
    fixed_number = 5
    if state["guesses"][-1] > fixed_number: 
        print("Higher than the target")
        state['upper_bound'] = state["guesses"][-1]
    elif state["guesses"][-1] < fixed_number: 
        print("Lower than the target")
        state["lower_bound"] = state["guesses"][-1]
    elif state["guesses"][-1] == fixed_number: 
        print("correct with the target")

    return state

# the decision node 
def decide(state: AgentState): 
    if state["guesses"][-1] == 5 or state["attempts"] >= 7: 
        return "end"
    else: 
        return "generate"


graph = StateGraph(AgentState)

graph.add_node("generate", generator)
graph.add_node("hint", hint)
graph.add_node("greeter", greeter)

graph.add_edge(START, "greeter")
graph.add_edge("greeter", "generate")
graph.add_edge("generate", "hint")

graph.add_conditional_edges(
    "hint", 
    decide, 
    {
        "generate": "generate", 
        "end": END
    }
)

app = graph.compile()

problem = AgentState(
    player_name="Oladimeji", 
    guesses=[],
    attempts=0, 
    lower_bound=0, 
    upper_bound=20
)

solution = app.invoke(problem)
print(solution)