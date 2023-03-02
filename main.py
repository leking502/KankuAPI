from fastapi import FastAPI
from pydantic import BaseModel
import openai

app = FastAPI()
openai.api_key = ''

conversation = []


class Message(BaseModel):
    text: str


@app.get("/opanai/gpt-3/reset")
async def reset_conversation():
    conversation.clear()
    return {"message": f"{'success'}"}


@app.post("/opanai/gpt-3/message")
async def send_message(message: Message):
    conversation.append({"role": "user", "content": f"{message}"})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )
    if len(conversation) > 10:
        conversation.clear()
        return {"message": f"{response['choices'][0]['message']['content']}"+"(对话长度过长已自动清除之前的对话)"}
    conversation.append({"role": "assistant", "content": f"{response['choices'][0]['message']['content']}"})
    print(response)
    return {"message": f"{response['choices'][0]['message']['content']}"}
