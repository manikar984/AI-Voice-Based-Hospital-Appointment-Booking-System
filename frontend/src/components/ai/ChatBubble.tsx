interface Message {

    id: number;

    sender: "ai" | "patient";

    text: string;

}

interface ChatBubbleProps {

    message: Message;

}

function ChatBubble({

    message,

}: ChatBubbleProps) {

    return (

        <div
            className={`flex ${
                message.sender === "ai"
                    ? "justify-start"
                    : "justify-end"
            }`}
        >

            <div
                className={`max-w-[75%] rounded-3xl px-5 py-4 shadow-md transition-all duration-200 ${
                    message.sender === "ai"
                        ? "bg-white border border-gray-200"
                        : "bg-blue-600 text-white"
                }`}
            >

                <div className="flex items-center gap-2 mb-2">

                    <div className="text-lg">

                        {message.sender === "ai"
                            ? "🤖"
                            : "👤"}

                    </div>

                    <span className="font-semibold text-sm">

                        {message.sender === "ai"
                            ? "AI Receptionist"
                            : "You"}

                    </span>

                </div>

                <p>

                    {message.text}

                </p>

            </div>

        </div>

    );

}

export default ChatBubble;