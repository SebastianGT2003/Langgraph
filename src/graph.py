from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from config import tools, memory, llm_with_tools
from state import State


def buid_graph () -> StateGraph:
    graph_builder= StateGraph(State)
    
    def chatbot(state: State):
        message = llm_with_tools.invoke(state["messages"])
        return {"messages": [message]}
    
    graph_builder.add_node("chatbot", chatbot)
    
    tool_node= ToolNode(tools)
    
    graph_builder.add_node("tools", tool_node)
    
    graph_builder.add_conditional_edges("chatbot", tools_condition)
    
    graph_builder.add_edge("tools", "chatbot")
    
    graph_builder.add_edge(START, "chatbot")
    
    return graph_builder.compile(checkpointer=memory)