from .langgraph_workflow import chatbot_app
from langchain_core.messages import HumanMessage

async def chat_with_langgraph_memory(user_id, message):
    input_messages = [HumanMessage(content=message)]
    input_data = {"messages": input_messages}
    result = chatbot_app.invoke(input_data, {"configurable": {"thread_id": user_id}})
    ai_message = result["messages"][-1]
    return {"response": ai_message.content, "memory": [msg.content for msg in result["messages"]]}
