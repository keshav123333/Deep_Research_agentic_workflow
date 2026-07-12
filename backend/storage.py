import json 
import os
import copy
from langchain_core.messages import HumanMessage, AIMessage
import uuid
import markdown
from weasyprint import HTML

DATA_DIR = "data"
CHAT_DIR = "data/chats"

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(CHAT_DIR, exist_ok=True)

THREAD_FILE = f"{DATA_DIR}/threads.json"

if not os.path.exists(THREAD_FILE):
    with open(THREAD_FILE,"w") as f:
        json.dump([],f)



def create_thread():
    thread_id=str(uuid.uuid4())
    with open(THREAD_FILE,"r") as f:
        threads=json.load(f)
    
    threads.append({
        "thread_id":thread_id,
        "title":"new_chat",
        "research":0
    })

    with open(THREAD_FILE,"w") as f:
        json.dump(threads,f,indent=2)
    return thread_id


def get_threads():
    with open(THREAD_FILE,"r") as f:
        return json.load(f)
    

def load_chat(chatbot,thread_id):
    msgs=chatbot.get_state(config={"configurable":{"thread_id":thread_id}}).values.get("messages",[])
    messages=[]
    need_thread={}
    with open(THREAD_FILE,"r") as f:
        threads=json.load(f)
    for thread in threads:
        if thread["thread_id"]==thread_id:
            need_thread=thread

    for msg in msgs:
        if isinstance(msg,HumanMessage):
            messages.append({
                "role":"human",
                "content":msg.content
            })
        elif isinstance(msg,AIMessage):
            messages.append({
                "role":"ai",
                "content":msg.content
            })
    return {"messages":messages,"thread":need_thread}



            

def get_specific_thread(thread_id):
    with open(THREAD_FILE,"r") as f:
        threads=json.load(f)
    ans=None
    for thread in threads:
        if thread["thread_id"]==thread_id:
            ans=copy.deepcopy(thread)
            thread["research"]=1
            with open(THREAD_FILE,"w") as f:
                json.dump(threads,f,indent=2)
            return ans
             
    return ans








# pip install fastapi uvicorn markdown weasyprint
def create_download(req: list[str],thread_id):
    filename = f"{uuid.uuid4()}.pdf"

    filepath = os.path.join(
        "pdfs",
        filename
    )

    # Merge all markdown strings
    markdown_text = "\n\n".join(req)

    # Markdown -> HTML
    html_content = markdown.markdown(
        markdown_text,
        extensions=[
            "tables",
            "fenced_code"
        ]
    )

    # Optional styling
    html_template = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial;
                margin: 40px;
                line-height: 1.6;
            }}

            h1 {{
                color: #222;
            }}

            h2 {{
                color: #444;
            }}

            code {{
                background: #f5f5f5;
                padding: 2px 4px;
            }}

            table {{
                border-collapse: collapse;
                width: 100%;
            }}

            th, td {{
                border: 1px solid black;
                padding: 8px;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    # HTML -> PDF
    HTML(
        string=html_template
    ).write_pdf(filepath)


    download_url= f"http://localhost:8000/pdfs/{filename}"

    with open(THREAD_FILE,"r") as f:
        threads=json.load(f)

    for thread in threads:
        if thread["thread_id"]==thread_id:
            thread["download"]=download_url
            with open(THREAD_FILE,"w") as f:
                json.dump(threads,f,indent=2)
            return download_url 

    

