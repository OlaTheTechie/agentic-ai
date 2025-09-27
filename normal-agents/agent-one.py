from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from typing import TypedDict, List
from dotenv import load_dotenv


load_dotenv()

class AgentState(TypedDict): 
    messages: List[HumanMessage]

llm = ChatGroq(model="llama-3.3-70b-versatile")

def process(state: AgentState) -> AgentState: 
    response = llm.invoke(state["messages"])
    print(f"\nAI: \n{response.content}")
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)

app = graph.compile()

user_input = input("Enter your message here: ")

response = app.invoke(input={"messages": [HumanMessage(content=user_input)]})
# print(response)