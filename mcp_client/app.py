from typing import List
from typing_extensions import TypedDict
from typing import Annotated
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_mcp_adapters.prompts import load_mcp_prompt
import asyncio

client = MultiServerMCPClient(
    {
        "math": {
            "command": "mcp",
            "args": ["run", "mcp_server/srv.py"],
            "transport": "stdio",
        },
        "bmi": {
            # "command": "mcp",
            # "args": ["run", "mcp_server/bmi_srv.py"],
            # "transport": "stdio",
            "url": "http://localhost:8000/mcp",
            "transport": "streamable_http",
        }
    }
)

import os

async def create_graph(math_session, bmi_session):
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0, api_key=os.getenv("GOOGLE_API_KEY"))

    math_tools = await load_mcp_tools(math_session)
    bmi_tools = await load_mcp_tools(bmi_session)
    tools = math_tools + bmi_tools
    llm_with_tool = llm.bind_tools(tools)

    system_prompt = await load_mcp_prompt(math_session, "system_prompt")
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt[0].content),
        MessagesPlaceholder("messages")
    ])
    chat_llm = prompt_template | llm_with_tool

    # State Management
    class State(TypedDict):
        messages: Annotated[List[AnyMessage], add_messages]

    # Nodes
    def chat_node(state: State) -> State:
        state["messages"] = chat_llm.invoke({"messages": state["messages"]})
        return state

    # Building the graph
    graph_builder = StateGraph(State)
    graph_builder.add_node("chat_node", chat_node)
    graph_builder.add_node("tool_node", ToolNode(tools=tools))
    graph_builder.add_edge(START, "chat_node")
    graph_builder.add_conditional_edges("chat_node", tools_condition, {"tools": "tool_node", "__end__": END})
    graph_builder.add_edge("tool_node", "chat_node")
    graph = graph_builder.compile(checkpointer=MemorySaver())
    return graph


async def main():
    config = {"configurable": {"thread_id": 1234}}
    async with client.session("math") as math_session, client.session("bmi") as bmi_session:
        agent = await create_graph(math_session, bmi_session)
        while True:
            message = input("User: ")
            response = await agent.ainvoke({"messages": message}, config=config)
            print("AI: " + response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())