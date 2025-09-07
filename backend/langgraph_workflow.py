from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, AIMessage
from backend.config import GOOGLE_API_KEY


# Initialize Gemini LLM instance
llm = ChatGoogleGenerativeAI(api_key=GOOGLE_API_KEY, model="gemini-2.0-flash", temperature=0,max_tokens=1024)


# Define the node function wrapper that LangGraph expects
def llm_node(state: dict) -> dict:
    messages = state.get("messages", [])
    response = llm.invoke(messages)
    if not isinstance(response, AIMessage):
        response = AIMessage(content=str(response))
    new_messages = messages + [response]
    return {"messages": new_messages}


def build_langgraph_app():
    builder = StateGraph(state_schema=MessagesState)
    builder.add_node("llm", llm_node)
    builder.add_edge(START, "llm")
    builder.add_edge("llm", END)
    memory = MemorySaver()
    return builder.compile(checkpointer=memory)


# Instantiate chatbot app
chatbot_app = build_langgraph_app()
