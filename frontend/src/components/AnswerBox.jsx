import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";


function AnswerBox({ answer }) {

    if (!answer) return null;

    return (
        <div className="mt-8">

            <h2 className="text-2xl font-bold mb-3">
                Answer
            </h2>

            <div className="
                bg-gray-100 
                rounded-lg 
                p-5
                prose
                max-w-none
            ">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {answer}
                </ReactMarkdown>
            </div>

        </div>
    );
}

export default AnswerBox;