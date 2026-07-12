import { useEffect, useState } from "react";
import Sidebar from "./components/Sidebar";
import ChatWindow from "./components/ChatWindow";
import api from "./api";

function App() {

    const [chatList, setChatList] = useState([]);

    const [currentThread, setCurrentThread] = useState(null);

    const [messages, setMessages] = useState([]);
    const [research,setResearch]=useState([])

    useEffect(() => {
        loadChats();
    }, []);

    const loadChats = async () => {

        const res = await api.get("/chat/list");

        setChatList(res.data);
    };

    const createChat = async () => {

        const res = await api.post("/chat/create");

        const newThread = {
            thread_id: res.data.thread_id,
            title: "New Chat"
        };

        setChatList(prev => [...prev, newThread]);

        setCurrentThread(res.data.thread_id);

        setMessages([]);
    };

    const loadChat = async (threadId) => {

        const res = await api.get(`/chat/${threadId}`);


        setCurrentThread(threadId);

        setMessages(res.data.messages);
    };

    const sendMessage = async (text) => {

        if (!currentThread) {
            alert("Create Chat First");
            return;
        }

        const userMessage = {
            role: "user",
            content: text
        };

        setMessages(prev => [
            ...prev,
            userMessage
        ]);

        const res = await api.post(
            "/chat/message",
            {
                thread_id: currentThread,
                message: text
            }
        );

        const aiMessage = {
            role: "assistant",
            content: res.data.response
        };

        setMessages(prev => [
            ...prev,
            aiMessage
        ]);
    };

    return (
        <div
            style={{
                display: "flex",
                height: "100vh"
            }}
        >
            <Sidebar
                chatList={chatList}
                createChat={createChat}
                loadChat={loadChat}
            />

            <ChatWindow
                messages={messages}
                sendMessage={sendMessage}
                research={research}
                
            />
        </div>
    );
}

export default App;