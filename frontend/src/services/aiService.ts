import API from "./api";

export const getAIStatus = async () => {
    const response = await API.get("/ai/status");
    return response.data;
};

export const getAIMemory = async () => {
    const response = await API.get("/ai/memory");
    return response.data;
};

export const getAITranscript = async () => {
    const response = await API.get("/ai/transcript");
    return response.data;
};

export const startAI = async () => {
    const response = await API.post("/ai/start");
    return response.data;
};

export const stopAI = async () => {

    const response = await API.post("/ai/stop");

    return response.data;

};

export const clearAI = async () => {

    const response = await API.post("/ai/clear");

    return response.data;

};

export const sendChatMessage = async (message: string) => {

    const response = await API.post("/ai/chat", {
        message,
    });

    return response.data;

};

