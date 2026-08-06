import { useState } from "react";

function ChatInput({ onAsk }) {

  const [question, setQuestion] = useState("");

  function handleSubmit() {

    if (!question.trim()) return;

    onAsk(question);

    setQuestion("");
  }

  function handleKeyDown(e) {

    if (e.key === "Enter" && !e.shiftKey) {

      e.preventDefault();

      handleSubmit();
    }

  }

  return (

    <div className="bg-white border-t p-4">

      <div className="max-w-4xl mx-auto flex gap-3">

        <textarea
          className="flex-1 border rounded-xl p-3 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
          rows={2}
          placeholder="Ask anything about Docker, Kubernetes, Linux..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyDown}
        />

        <button
          onClick={handleSubmit}
          className="px-6 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-semibold"
        >
          Send
        </button>

      </div>

    </div>

  );

}

export default ChatInput;