from pydantic import BaseModel
import asyncio
from ragagent.application.conversation_service.generate_response import (
    get_response,
)
from ragagent.application.conversation_service.reset_conversation import (
    reset_conversation_state,
)

class ChatMessage(BaseModel):
    message: str

async def chat(chat_message: ChatMessage):
    try:
        response, _ = await get_response(
            messages=chat_message.message,
        )
        return {"response": response}
    except Exception as e:
        raise Exception(str(e))

if __name__ == "__main__":
    asyncio.run(reset_conversation_state())
    print("Welcome to the Chatbot! Type 'q', 'stop', or 'exit' to quit.")
    while True:
        user = ChatMessage(message=input("Enter your query: "))
        if user.message.lower() in['q', 'stop', "exit"]:
            break
        else:
            result = asyncio.run(chat(user))
            print(result['response'])