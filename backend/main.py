import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from graph import chatbot
from langchain_core.messages import HumanMessage, AIMessage

 
from storage import (
    create_thread,
    get_specific_thread,
    get_threads,
    load_chat,
     create_download
)
from research_storage import (add_to_vector_store, get_text)
from research_chatbot import research_chatbot

from langchain_core.messages import HumanMessage

app=FastAPI()

os.makedirs("pdfs", exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.mount(
    "/pdfs",
    StaticFiles(directory="pdfs"),
    name="pdfs"
)

class ChatRequest(BaseModel):
    thread_id:str
    message:str


@app.post("/chat/create")
def create_chat():

    thread_id = create_thread()

    return {
        "thread_id": thread_id
    }


@app.get("/chat/list")
def list_chats():

    return get_threads()

@app.get("/chat/{thread_id}")
def get_chat(thread_id: str):

    return load_chat(chatbot,thread_id)

@app.post("/chat/message")
def chat(req: ChatRequest):
    thread_info=get_specific_thread(req.thread_id)
    if thread_info["research"]==0:
         
         res=research_chatbot.invoke({"query":req.message})
         print(res)
         text=get_text(res["final_ans"])
         add_to_vector_store(text)
         download_link=create_download(res["final_ans"],req.thread_id)
          
         model_res= f'<a href="{download_link}" target="_blank" rel="noreferrer">Download PDF</a>'
         res=chatbot.invoke({"messages":[HumanMessage(content=req.message),AIMessage(content=model_res)]},config={"configurable":{"thread_id":req.thread_id}})
         print(load_chat(chatbot,req.thread_id))
         return {
             "response": f"here is your research report : {download_link}"
         }
         

         
    else:
    
        response=chatbot.invoke({"messages":[HumanMessage(content=req.message)]},config={"configurable":{"thread_id":req.thread_id}})
        res=response["messages"][-1].content
        return {
        "response": res[0]["text"]
    }
