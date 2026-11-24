function TypingIndicator() {
    return (
        <div className="flex items-center gap-2 text-gray-500 text-sm py-2">
            <span className="animate-pulse">●</span>
            <span className="animate-pulse delay-150">●</span>
            <span className="animate-pulse delay-300">●</span>

            <span className="ml-2">
                AI is typing...
            </span>
        </div>
    );
}

export default TypingIndicator;