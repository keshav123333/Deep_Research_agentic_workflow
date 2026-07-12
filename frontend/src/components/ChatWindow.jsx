import { useState } from "react";

function ChatWindow({
    messages,
    sendMessage
}) {

    const [input, setInput] =
        useState("");

    const handleSend = () => {

        if (!input.trim())
            return;

        sendMessage(input);

        setInput("");
    };

    return (
        <div
            style={{
                flex: 1,
                display: "flex",
                flexDirection: "column"
            }}
        >

            <div
                style={{
                    flex: 1,
                    overflowY: "auto",
                    padding: "20px"
                }}
            >

                {
                    messages.map(
                        (msg, index) => (

                            <div
                                key={index}
                                style={{
                                    marginBottom:
                                        "15px"
                                }}
                            >
                                <b>
                                    {msg.role}
                                </b>

                                <p>
                                    {msg.content}
                                </p>
                            </div>
                        )
                    )
                }

            </div>

            <div
                style={{
                    display: "flex",
                    padding: "10px"
                }}
            >
                <input
                    value={input}
                    onChange={(e) =>
                        setInput(
                            e.target.value
                        )
                    }
                    style={{
                        flex: 1
                    }}
                />

                <button
                    onClick={
                        handleSend
                    }
                >
                    Send
                </button>
            </div>

        </div>
    );
}

export default ChatWindow;