import { useState } from "react";
import { Card } from "@/components/ui/card";
import { useEffect } from "react";
import {
    getAIStatus,
    getAIMemory,
    getAITranscript,
    startAI,
    stopAI,
    clearAI,
    sendChatMessage
} from "@/services/aiService";
import ChatBubble from "@/components/ai/ChatBubble";
import ChatHeader from "@/components/ai/ChatHeader";
import ChatInput from "@/components/ai/ChatInput";
import PatientPanel from "@/components/ai/PatientPanel";
import TypingIndicator from "@/components/ai/TypingIndicator";

interface Message {
    id: number;
    sender: "ai" | "patient";
    text: string;
}

interface ConversationMemory {
    intent?: string;
    doctor?: string;
    date?: string;
    time?: string;
    phone?: string;
    patient_name?: string;
}

function AIAgentPage() {

    const [status, setStatus] = useState("Online");

    const [chatInput, setChatInput] = useState("");

  const [messages, setMessages] = useState<Message[]>([]);


  const [memory, setMemory] = useState<ConversationMemory>({
      intent: "--",
      doctor: "--",
      date: "--",
      time: "--",
      phone: "--"
  });

  const [aiStats, setAIStats] = useState({
      live_calls: 0,
      calls_today: 0,
      bookings_today: 0,
      success_rate: 0,
      avg_response: "",
      avg_call_duration: ""
  });

  useEffect(() => {

      const loadAIStatus = async () => {

          try {

              const data = await getAIStatus();

              setStatus(data.status);

              setAIStats({
                  live_calls: data.live_calls,
                  calls_today: data.calls_today,
                  bookings_today: data.bookings_today,
                  success_rate: data.success_rate,
                  avg_response: data.avg_response,
                  avg_call_duration: data.avg_call_duration,
              });

              const memoryData = await getAIMemory();

                setMemory(memoryData);

              const transcriptData = await getAITranscript();

                setMessages(transcriptData);

          } catch (error) {

              console.error(error);

          }

      };

      loadAIStatus();

  }, []);

  const handleStartListening = async () => {

        setStatus("Listening");

        try {

            const result = await startAI();

            const transcript = await getAITranscript();

            setMessages(transcript);

            setMemory(result.memory);

            setStatus("Online");

        } catch (error) {

            console.error(error);

            setStatus("Online");

        }

    };

  async function handleStopListening() {

      try {

          await stopAI();

          setStatus("Offline");

      } catch (error) {

          console.error(error);

      }

  }

  function handleMicStop() {

    setStatus("Online");

}

  async function handleClearConversation() {

      try {

          await clearAI();

          setMessages([]);

          setMemory({
              intent: "--",
              doctor: "--",
              date: "--",
              time: "--",
              phone: "--",
              patient_name: "--",
          });


          setStatus("Offline");

      } catch (error) {

          console.error(error);

      }

  }
  
  async function handleSendMessage() {

      if (!chatInput.trim()) return;

      try {

          const result = await sendChatMessage(chatInput);

            setStatus("Online");

          setMessages((prev) => [
              ...prev,
              {
                  id: Date.now(),
                  sender: "patient",
                  text: chatInput,
              },
              {
                  id: Date.now() + 1,
                  sender: "ai",
                  text: result.response
              },
          ]);

          setMemory(result.memory);

          setChatInput("");

      } catch (error) {

          console.error(error);

      }

  }

  return (

    <div className="space-y-6">

      <Card className="p-6">

        <div className="flex items-center justify-between mb-6">

          <span
            className={`rounded-full px-4 py-2 font-semibold ${
              status === "Listening"
                ? "bg-green-100 text-green-700"
                : status === "Offline"
                ? "bg-red-100 text-red-700"
                : "bg-yellow-100 text-yellow-700"
            }`}
          >
            Status: {status}
          </span>

        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">

          <div className="rounded-lg border p-4">
            <p className="text-sm text-gray-500">Live Calls</p>
            <p className="text-2xl font-bold text-blue-600">{aiStats.live_calls}</p>
          </div>

          <div className="rounded-lg border p-4">
            <p className="text-sm text-gray-500">Calls Today</p>
            <p className="text-2xl font-bold">{aiStats.calls_today}</p>
          </div>

          <div className="rounded-lg border p-4">
            <p className="text-sm text-gray-500">Bookings Today</p>
            <p className="text-2xl font-bold text-green-600">{aiStats.bookings_today}</p>
          </div>

          <div className="rounded-lg border p-4">
            <p className="text-sm text-gray-500">Success Rate</p>
            <p className="text-2xl font-bold">{aiStats.success_rate}%</p>
          </div>

          <div className="rounded-lg border p-4">
            <p className="text-sm text-gray-500">Avg Response</p>
            <p className="text-2xl font-bold">{aiStats.avg_response}</p>
          </div>

          <div className="rounded-lg border p-4">
            <p className="text-sm text-gray-500">Avg Call</p>
            <p className="text-2xl font-bold">{aiStats.avg_call_duration}</p>
          </div>

        </div>

      </Card>

      <div className="grid grid-cols-[1fr_320px] gap-6">

          <Card className="flex flex-col h-[650px] p-0 overflow-hidden">

            <div className="border-b p-6">

                <ChatHeader
                    status={status}
                    handleStopListening={handleStopListening}
                    handleClearConversation={handleClearConversation}
                />

            </div>

            <div className="flex-1 overflow-y-auto p-6 space-y-5">

                {messages.map((message) => (

                    <ChatBubble
                        key={message.id}
                        message={message}
                    />

                ))}

                {status === "Listening" && (
                    <TypingIndicator />
                )}

            </div>

            <div className="border-t p-4 bg-white">

                <ChatInput
                    chatInput={chatInput}
                    setChatInput={setChatInput}
                    handleSendMessage={handleSendMessage}
                    handleStartListening={handleStartListening}
                    handleStopListening={handleStopListening}
                    handleMicStop={handleMicStop}
                />

            </div>

            </Card>

            <PatientPanel
                memory={memory}
            />

      </div>

    </div>

  );

}

export default AIAgentPage;