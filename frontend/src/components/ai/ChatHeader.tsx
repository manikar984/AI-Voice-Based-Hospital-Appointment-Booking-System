import { Square, Trash2, Bot } from "lucide-react";
import { Button } from "@/components/ui/button";

interface ChatHeaderProps {
    status: string;
    handleStopListening: () => void;
    handleClearConversation: () => void;
}

function ChatHeader({
    status,
    handleStopListening,
    handleClearConversation,
}: ChatHeaderProps) {
    return (
        <div className="flex items-start justify-between">

            <div>

                <div className="flex items-center gap-3">

                    <Bot className="h-8 w-8 text-blue-600" />

                    <h1 className="text-3xl font-bold">
                        AI Hospital Receptionist
                    </h1>

                </div>

                <p className="text-gray-500 mt-2">
                    Your intelligent healthcare assistant
                </p>

            </div>

            <div className="flex items-center gap-3">

                <span
                    className={`rounded-full px-3 py-1 text-sm font-medium ${
                        status === "Listening" || status === "Online"
                            ? "bg-green-100 text-green-700"
                            : "bg-red-100 text-red-600"
                    }`}
                >
                    {status}
                </span>

                <Button
                    variant="outline"
                    size="sm"
                    onClick={handleStopListening}
                >
                    <Square className="mr-2 h-4 w-4" />
                    Stop
                </Button>

                <Button
                    variant="destructive"
                    size="sm"
                    onClick={handleClearConversation}
                >
                    <Trash2 className="mr-2 h-4 w-4" />
                    Clear
                </Button>

            </div>

        </div>
    );
}

export default ChatHeader;