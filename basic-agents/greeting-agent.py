from typing import TypedDict
from langgraph.graph import StateGraph


# define the state of the graph 
class Message(TypedDict): 
    message: str

# node 
def greeting_node(state: Message) -> Message: 
    state['message'] = state['message'] + ", you're doing an amazing job learning langgraph."
    return state

# building the graph
graph = StateGraph(state_schema=Message)
graph.add_node("greeter", greeting_node)
graph.set_entry_point("greeter")
graph.set_finish_point("greeter")

# compile graph
app = graph.compile()

# testing the graph 
message = Message(message="Bob")
result = app.invoke(message)
print(result)