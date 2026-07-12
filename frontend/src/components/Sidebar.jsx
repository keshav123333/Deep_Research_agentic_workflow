function Sidebar({
    chatList,
    createChat,
    loadChat
}) {

    return (
        <div
            style={{
                width: "250px",
                borderRight: "1px solid gray",
                padding: "10px"
            }}
        >
            <button
                onClick={createChat}
            >
                New Chat
            </button>

            <hr />

            {
                chatList.map(chat => (

                    <div
                        key={chat.thread_id}
                        onClick={() =>
                            loadChat(
                                chat.thread_id
                            )
                        }
                        style={{
                            cursor: "pointer",
                            marginTop: "10px"
                        }}
                    >
                        {chat.title}
                    </div>
                ))
            }
        </div>
    );
}

export default Sidebar;