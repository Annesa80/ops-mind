import { useState, useEffect } from "react";

import ChatInput from "./components/ChatInput";
import ChatWindow from "./components/ChatWindow";
import FileUpload from "./components/FileUpload";

import { askOpsMind, resetConversationId } from "./api/opsmind";

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

    localStorage.removeItem(
      "opsmind-history"
    );

    resetConversationId();
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
        content: "",
        sources: []
      }
    ]);

    try {

      await askOpsMind(
        question,
        (event) => {

          if (event.type === "token") {

            setMessages(prev => {

              const updated = [...prev];

              const lastIndex =
                updated.length - 1;

              updated[lastIndex] = {
                ...updated[lastIndex],
                content:
                  updated[lastIndex].content +
                  event.content
              };

              return updated;

            });

          }

          if (event.type === "sources") {

            setMessages(prev => {

              const updated = [...prev];

              const lastIndex =
                updated.length - 1;

              updated[lastIndex] = {
                ...updated[lastIndex],
                sources: event.sources
              };

              return updated;

            });

          }

        }
      );

    } catch (err) {

      console.error(err);

      setMessages(prev => {

        const updated = [...prev];

        const lastIndex =
          updated.length - 1;

        updated[lastIndex] = {
          ...updated[lastIndex],
          content:
            "Something went wrong. Please try again."
        };

        return updated;

      });

    } finally {

      setLoading(false);

    }
  }

  return (

    <div className="min-h-screen bg-slate-100 flex flex-col">

      {/* Main white application window */}

      <main
        className="
          w-full
          max-w-5xl
          mx-auto
          flex-1
          bg-white
          border-x
          border-slate-200
          shadow-sm
        "
      >

        {/* Header */}

        <header className="px-6 pt-10 pb-6">

          <div className="flex items-center justify-between">

            {/* Branding */}

            <div className="flex items-center gap-3">

              <div
                className="
                  w-11
                  h-11
                  rounded-xl
                  bg-blue-600
                  flex
                  items-center
                  justify-center
                  text-2xl
                  shadow-sm
                "
              >
                🤖
              </div>

              <div>

                <h1 className="text-3xl font-bold text-slate-900">
                  OpsMind
                </h1>

                <p className="text-sm text-slate-500">
                  DevOps AI Assistant
                </p>

              </div>

            </div>


            {/* Actions */}

            <div className="flex items-center gap-2">

              <FileUpload />

              <button
                onClick={newChat}
                className="
                  px-4
                  py-2
                  rounded-lg
                  border
                  border-slate-300
                  bg-white
                  text-slate-700
                  text-sm
                  font-medium
                  hover:bg-slate-50
                  transition
                "
              >
                + New Chat
              </button>

            </div>

          </div>

        </header>


        {/* Divider */}

        <div className="border-t border-slate-200" />


        {/* Chat */}

        <section className="px-6 py-8">

          {messages.length === 0 ? (

            <div className="min-h-[55vh] flex flex-col items-center justify-center text-center">

              <div className="text-5xl mb-5">
                🤖
              </div>

              <h2 className="text-2xl font-semibold text-slate-800">
                How can I help with your DevOps problem?
              </h2>

              <p className="mt-2 max-w-lg text-slate-500">
                Ask about Docker, Kubernetes, Linux, Redis,
                Nginx, or upload your own knowledge files.
              </p>

              <div className="mt-6 flex flex-wrap justify-center gap-2">

                {[
                  "Why is my Kubernetes pod crashing?",
                  "How do I fix Redis MISCONF?",
                  "How do I troubleshoot Nginx 502?"
                ].map((suggestion) => (

                  <button
                    key={suggestion}
                    onClick={() => handleAsk(suggestion)}
                    className="
                      px-4
                      py-2
                      rounded-full
                      border
                      border-slate-200
                      bg-slate-50
                      text-sm
                      text-slate-600
                      hover:border-blue-300
                      hover:bg-blue-50
                      hover:text-blue-600
                      transition
                    "
                  >
                    {suggestion}
                  </button>

                ))}

              </div>

            </div>

          ) : (

            <ChatWindow messages={messages} />

          )}


          {/* Thinking indicator */}

          {loading && (

            <div className="flex items-center gap-2 mt-6 text-sm text-slate-500">

              <div className="flex gap-1">

                <span className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" />
                <span className="w-2 h-2 bg-blue-500 rounded-full animate-bounce [animation-delay:150ms]" />
                <span className="w-2 h-2 bg-blue-500 rounded-full animate-bounce [animation-delay:300ms]" />

              </div>

              OpsMind is thinking...

            </div>

          )}

        </section>


        {/* Input */}

        <section className="px-6 pb-8">

          <ChatInput
            onAsk={handleAsk}
          />

        </section>

      </main>


      {/* Footer */}

      <footer className="py-5 text-center">

        <p className="text-sm text-slate-400">
          © 2026 OpsMind · DevOps AI Assistant
        </p>

      </footer>

    </div>

  );

}


export default App;