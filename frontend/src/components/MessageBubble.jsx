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
            : "bg-white border border-slate-200"
        }`}
      >

        {isUser ? (

          <p className="leading-7">
            {content}
          </p>

        ) : (

          <div className="max-w-none text-slate-800">

            <ReactMarkdown
              remarkPlugins={[remarkGfm]}

              components={{

                /* ----------------------------- */
                /* PARAGRAPHS */
                /* ----------------------------- */

                p({ children }) {
                  return (
                    <p className="mb-4 last:mb-0 leading-7">
                      {children}
                    </p>
                  );
                },


                /* ----------------------------- */
                /* INLINE CODE */
                /* ----------------------------- */

                code({ className, children, ...props }) {

                  const isBlock =
                    className?.includes("language-");

                  if (!isBlock) {
                    return (
                      <code
                        className="
                          inline-block
                          font-mono
                          text-sm
                          bg-slate-100
                          text-slate-900
                          px-1.5
                          py-0.5
                          rounded
                          border
                          border-slate-200
                        "
                        {...props}
                      >
                        {children}
                      </code>
                    );
                  }

                  return (
                    <code
                      className="
                        block
                        font-mono
                        text-sm
                        leading-6
                        text-slate-100
                      "
                      {...props}
                    >
                      {children}
                    </code>
                  );
                },


                /* ----------------------------- */
                /* CODE BLOCK */
                /* ----------------------------- */

                pre({ children }) {
                  return (
                    <pre
                      className="
                        my-4
                        p-4
                        rounded-lg
                        bg-slate-950
                        text-slate-100
                        overflow-x-auto
                        border
                        border-slate-800
                      "
                    >
                      {children}
                    </pre>
                  );
                },


                /* ----------------------------- */
                /* UNORDERED LIST */
                /* ----------------------------- */

                ul({ children }) {
                  return (
                    <ul className="list-disc ml-6 mb-4 space-y-2">
                      {children}
                    </ul>
                  );
                },


                /* ----------------------------- */
                /* ORDERED LIST */
                /* ----------------------------- */

                ol({ children }) {
                  return (
                    <ol className="list-decimal ml-6 mb-4 space-y-2">
                      {children}
                    </ol>
                  );
                },


                /* ----------------------------- */
                /* LIST ITEM */
                /* ----------------------------- */

                li({ children }) {
                  return (
                    <li className="leading-7">
                      {children}
                    </li>
                  );
                },


                /* ----------------------------- */
                /* HEADINGS */
                /* ----------------------------- */

                h1({ children }) {
                  return (
                    <h1 className="text-2xl font-bold mt-6 mb-3">
                      {children}
                    </h1>
                  );
                },

                h2({ children }) {
                  return (
                    <h2 className="text-xl font-bold mt-6 mb-3">
                      {children}
                    </h2>
                  );
                },

                h3({ children }) {
                  return (
                    <h3 className="text-lg font-semibold mt-5 mb-2">
                      {children}
                    </h3>
                  );
                },


                /* ----------------------------- */
                /* LINKS */
                /* ----------------------------- */

                a({ href, children }) {
                  return (
                    <a
                      href={href}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:underline"
                    >
                      {children}
                    </a>
                  );
                },


                /* ----------------------------- */
                /* BLOCKQUOTE */
                /* ----------------------------- */

                blockquote({ children }) {
                  return (
                    <blockquote
                      className="
                        border-l-4
                        border-blue-300
                        pl-4
                        my-4
                        text-slate-600
                        italic
                      "
                    >
                      {children}
                    </blockquote>
                  );
                },

              }}
            >
              {content}
            </ReactMarkdown>

          </div>
        )}


        {/* ----------------------------- */}
        {/* SOURCES */}
        {/* ----------------------------- */}

        {!isUser && sources?.length > 0 && (

          <div className="mt-5 border-t border-slate-200 pt-3">

            <p className="font-bold text-sm mb-2">
              Sources
            </p>

            <ul className="space-y-2 text-sm">

              {sources.map((source, index) => (

                <li
                  key={`${source.type}-${source.title}-${index}`}
                  className="flex items-start gap-2"
                >

                  <span>📄</span>

                  {source.type === "web" && source.url ? (

                    <a
                      href={source.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:underline"
                    >
                      {source.title}
                    </a>

                  ) : (

                    <span className="text-slate-700">
                      {source.title}
                    </span>

                  )}

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