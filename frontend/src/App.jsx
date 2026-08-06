import { useState } from "react";
import { askOpsMind } from "./api/opsmind";

import ChatInput from "./components/ChatInput";
import AnswerBox from "./components/AnswerBox";
import SourceList from "./components/SourceList";


function App() {

  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);


  async function handleAsk(question) {

    setLoading(true);

    try {
      const data = await askOpsMind(question);

      setAnswer(data.answer);
      setSources(data.sources);

    } catch (err) {
      console.error(err);
      setAnswer("Something went wrong.");
    }

    setLoading(false);
  }


  return (
    <div className="min-h-screen bg-slate-100 flex justify-center py-10">

      <div className="w-full max-w-4xl bg-white rounded-xl shadow-lg p-8">

        <h1 className="text-4xl font-bold text-center">
          🤖 OpsMind
        </h1>

        <p className="text-center text-gray-500 mt-2">
          DevOps AI Assistant
        </p>


        <ChatInput onAsk={handleAsk}/>


        {loading && (
          <p className="text-center mt-6">
            🤖 Thinking...
          </p>
        )}


        <AnswerBox answer={answer}/>

        <SourceList sources={sources}/>

      </div>

    </div>
  );
}


export default App;