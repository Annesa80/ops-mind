import MessageBubble from "./MessageBubble";

function ChatWindow({ messages }) {
  return (
    <div className="flex flex-col gap-4">
      {messages.map((message, index) => (
        <MessageBubble
          key={index}
          role={message.role}
          content={message.content}
          sources={message.sources}
        />
      ))}
    </div>
  );
}

export default ChatWindow;