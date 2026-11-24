import { useEffect, useRef, useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Mic, MicOff, SendHorizontal } from "lucide-react";

interface ChatInputProps {
    chatInput: string;
    setChatInput: (value: string) => void;
    handleSendMessage: () => void;
    handleStartListening: () => void;
    handleStopListening: () => void;
    handleMicStop: () => void;
}

function ChatInput({
    chatInput,
    setChatInput,
    handleSendMessage,
    handleStartListening,
    handleStopListening,
    handleMicStop,
}: ChatInputProps) {

    const [isListening, setIsListening] = useState(false);
    const [barHeights, setBarHeights] = useState<number[]>(
        Array(24).fill(4)
    );

    const audioContextRef = useRef<AudioContext | null>(null);
    const analyserRef = useRef<AnalyserNode | null>(null);
    const streamRef = useRef<MediaStream | null>(null);
    const animationRef = useRef<number | null>(null);

    const stopVisualizer = () => {

        if (animationRef.current) {
            cancelAnimationFrame(animationRef.current);
            animationRef.current = null;
        }

        if (streamRef.current) {
            streamRef.current.getTracks().forEach((track) => track.stop());
            streamRef.current = null;
        }

        if (audioContextRef.current) {
            audioContextRef.current.close();
            audioContextRef.current = null;
        }

        analyserRef.current = null;
        setBarHeights(Array(24).fill(4));
        setIsListening(false);
    };

    const startVisualizer = async () => {

        try {

            const stream = await navigator.mediaDevices.getUserMedia({
                audio: true,
            });

            streamRef.current = stream;

            const audioContext = new AudioContext();
            audioContextRef.current = audioContext;

            await audioContext.resume();

            const analyser = audioContext.createAnalyser();
            analyser.fftSize = 256;

            analyserRef.current = analyser;

            const microphone =
                audioContext.createMediaStreamSource(stream);

            microphone.connect(analyser);

            const dataArray = new Uint8Array(
                analyser.frequencyBinCount
            );

            const updateVisualizer = () => {

                if (!analyserRef.current) return;

                analyserRef.current.getByteTimeDomainData(dataArray);

                const newBars: number[] = [];

                const samplesPerBar = Math.floor(
                    dataArray.length / 24
                );

                for (let i = 0; i < 24; i++) {

                    let sum = 0;

                    const start = i * samplesPerBar;
                    const end = start + samplesPerBar;

                    for (let j = start; j < end; j++) {

                        const value =
                            (dataArray[j] - 128) / 128;

                        sum += value * value;
                    }

                    const rms = Math.sqrt(
                        sum / samplesPerBar
                    );

                    const height = Math.min(
                        32,
                        Math.max(
                            4,
                            rms * 70
                        )
                    );

                    newBars.push(height);
                }

                setBarHeights(newBars);

                animationRef.current =
                    requestAnimationFrame(updateVisualizer);
            };

            updateVisualizer();

            setIsListening(true);

        } catch (error) {

            console.error("Microphone access error:", error);

            setIsListening(false);
        }
    };

    const handleMicClick = async () => {

        if (isListening) {

            stopVisualizer();

            handleMicStop();

        } else {

            await startVisualizer();

            handleStartListening();

        }
    };

    useEffect(() => {

        return () => {
            stopVisualizer();
        };

    }, []);

    

    return (
        <div className="space-y-4">

            <div className="flex items-center gap-3 rounded-full border bg-white px-4 py-3 shadow-lg">

                <Input
                    className="flex-1 border-0 shadow-none focus-visible:ring-0"
                    placeholder="Ask anything..."
                    value={chatInput}
                    onChange={(e) =>
                        setChatInput(e.target.value)
                    }
                    onKeyDown={(e) => {

                        if (e.key === "Enter") {
                            handleSendMessage();
                        }

                    }}
                />

                {isListening && (

                    <div className="flex items-center gap-[3px] h-8 w-32 overflow-hidden">

                        {barHeights.map((height, index) => (

                            <div
                                key={index}
                                className="w-[2px] rounded-full bg-blue-600 transition-all duration-75"
                                style={{
                                    height: `${height}px`,
                                }}
                            />

                        ))}

                    </div>

                )}

                <Button
                    variant="ghost"
                    size="icon"
                    onClick={handleMicClick}
                >
                    {isListening ? (
                        <MicOff className="h-5 w-5 text-red-600" />
                    ) : (
                        <Mic className="h-5 w-5" />
                    )}
                </Button>

                <Button
                    size="icon"
                    onClick={handleSendMessage}
                >
                    <SendHorizontal className="h-5 w-5" />
                </Button>

            </div>

        </div>
    );
}

export default ChatInput;