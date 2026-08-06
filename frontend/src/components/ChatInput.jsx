import { useState } from "react";


function ChatInput({onAsk}) {

    const [question,setQuestion] = useState("");


    return (
        <>
            <textarea
                className="w-full mt-8 border rounded-lg p-4 h-40"
                placeholder="Ask anything about Docker, Kubernetes, Linux..."
                value={question}
                onChange={(e)=>setQuestion(e.target.value)}
            />


            <button
                className="mt-4 w-full bg-blue-600 text-white py-3 rounded-lg"
                onClick={() => onAsk(question)}
            >
                Ask
            </button>
        </>
    );
}


export default ChatInput;