import axios from "axios";

export async function askOpsMind(question) {
    const response = await axios.post(
        "http://127.0.0.1:8000/chat",
        {
            question: question,
        }
    );

    return response.data;
}