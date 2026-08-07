import { useState, useEffect } from "react";
import { askOpsMind } from "./api/opsmind";

import ChatInput from "./components/ChatInput";
import ChatWindow from "./components/ChatWindow";

function App() {

  const [messages, setMessages] = useState(() => {
    const saved = localStorage.getItem("opsmind-history");
    return saved ? JSON.parse(saved) : [];
  });

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    localStorage.setItem(
      "opsmind-history",
      JSON.stringify(messages)
    );
  }, [messages]);

  function newChat() {
    setMessages([]);
    localStorage.removeItem("opsmind-history");
  }

  async function handleAsk(question) {

    setLoading(true);


    const history = [
      ...messages,
      {
        role: "user",
        content: question
      }
    ];


    setMessages(prev => [
      ...prev,
      {
        role: "user",
        content: question
      },
      {
        role: "assistant",
        content: ""
      }
    ]);


    try {

      await askOpsMind(
        [
          ...history
        ],
        (chunk) => {

          setMessages(prev => {

            const updated = [...prev];

            const lastIndex = updated.length - 1;


            updated[lastIndex] = {
              ...updated[lastIndex],
              content:
                updated[lastIndex].content + chunk
            };


            return updated;

          });

        }
      );


    } catch(err) {

      console.error(err);


      setMessages(prev => {

        const updated = [...prev];

        updated[updated.length - 1].content =
          "Something went wrong.";


        return updated;

      });

    }


    setLoading(false);
  }

  return (
    <div className="min-h-screen bg-slate-100 flex justify-center py-10">
      <div className="w-full max-w-4xl bg-white rounded-xl shadow-lg p-8 flex flex-col gap-6">
        <div>
          <h1 className="text-4xl font-bold text-center">
            🤖 OpsMind
          </h1>

          <p className="text-center text-gray-500 mt-2">
            DevOps AI Assistant
          </p>
        </div>

        <button
          onClick={newChat}
          className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg"
        >
          New Chat
        </button>

        <ChatWindow messages={messages} />

        {loading && (
          <p className="text-gray-500">
            🤖 Thinking...
          </p>
        )}

        <ChatInput onAsk={handleAsk} />
      </div>
    </div>
  );
}

export default App;