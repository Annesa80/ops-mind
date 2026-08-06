import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

function MessageBubble({ role, content, sources }) {
  const isUser = role === "user";

  return (
    <div
      className={`flex ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 shadow ${
          isUser
            ? "bg-blue-600 text-white"
            : "bg-white border"
        }`}
      >

        {isUser ? (
          <p>{content}</p>
        ) : (
          <div className="prose prose-slate max-w-none">
            <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                code({inline, children, ...props}) {

                    if (inline) {
                    return (
                        <code
                        className="bg-gray-200 text-black px-1 rounded"
                        {...props}
                        >
                        {children}
                        </code>
                    );
                    }

                    return (
                    <pre className="bg-gray-100 text-black p-4 rounded-lg overflow-x-auto">
                        <code {...props}>
                        {children}
                        </code>
                    </pre>
                    );
                }
                }}
            >
                {content}
            </ReactMarkdown>
            </div>
        )}

        {!isUser && sources?.length > 0 && (
          <div className="mt-4 border-t pt-3">
            <p className="font-bold text-sm mb-2">
              Sources
            </p>

            <ul className="list-disc list-inside text-sm">
              {sources.map((source) => (
                <li key={source}>
                  📄 {source}
                </li>
              ))}
            </ul>
          </div>
        )}

      </div>
    </div>
  );
}

export default MessageBubble;