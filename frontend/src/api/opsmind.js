const API_URL = "http://127.0.0.1:8000";

const CONVERSATION_KEY = "opsmind-conversation-id";


// ============================================================
// CONVERSATION ID
// ============================================================

function getConversationId() {

  let conversationId =
    localStorage.getItem(CONVERSATION_KEY);

  if (!conversationId) {

    conversationId =
      crypto.randomUUID();

    localStorage.setItem(
      CONVERSATION_KEY,
      conversationId
    );
  }

  return conversationId;
}


// ============================================================
// RESET CONVERSATION
// ============================================================

export function resetConversationId() {

  localStorage.removeItem(
    CONVERSATION_KEY
  );
}


// ============================================================
// CHAT STREAM
// ============================================================

export async function askOpsMind(
  question,
  onEvent
) {

  const conversationId =
    getConversationId();

  // ----------------------------------------------------------
  // Validate question
  // ----------------------------------------------------------

  if (
    typeof question !== "string" ||
    !question.trim()
  ) {

    throw new Error(
      "Question cannot be empty"
    );
  }


  // ----------------------------------------------------------
  // Send request
  // ----------------------------------------------------------

  const response = await fetch(
    `${API_URL}/chat`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        conversation_id:
          conversationId,

        question:
          question.trim(),
      }),
    }
  );


  // ----------------------------------------------------------
  // Handle FastAPI errors
  // ----------------------------------------------------------

  if (!response.ok) {

    let errorMessage =
      "Chat request failed";

    try {

      const errorData =
        await response.json();

      console.error(
        "FastAPI error:",
        errorData
      );

      errorMessage =
        JSON.stringify(
          errorData
        );

    } catch {
      // Ignore JSON parsing failure
    }

    throw new Error(
      `${response.status}: ${errorMessage}`
    );
  }


  // ----------------------------------------------------------
  // Streaming response
  // ----------------------------------------------------------

  if (!response.body) {

    throw new Error(
      "No response body"
    );
  }


  const reader =
    response.body.getReader();

  const decoder =
    new TextDecoder();

  let buffer = "";


  // ----------------------------------------------------------
  // Read stream
  // ----------------------------------------------------------

  while (true) {

    const {
      done,
      value
    } = await reader.read();


    if (done) {
      break;
    }


    buffer += decoder.decode(
      value,
      {
        stream: true
      }
    );


    const lines =
      buffer.split("\n");


    // Keep incomplete line
    buffer =
      lines.pop();


    for (const line of lines) {

      if (!line.trim()) {
        continue;
      }


      try {

        const event =
          JSON.parse(line);

        onEvent(event);

      } catch (error) {

        console.error(
          "Failed to parse stream event:",
          line
        );

      }

    }
  }


  // ----------------------------------------------------------
  // Process final buffered line
  // ----------------------------------------------------------

  if (buffer.trim()) {

    try {

      const event =
        JSON.parse(buffer);

      onEvent(event);

    } catch (error) {

      console.error(
        "Failed to parse final stream event:",
        buffer
      );

    }
  }
}


// ============================================================
// FILE UPLOAD
// ============================================================

export async function uploadDocument(file) {

  const formData =
    new FormData();

  formData.append(
    "file",
    file
  );


  const response =
    await fetch(
      `${API_URL}/upload`,
      {
        method: "POST",
        body: formData,
      }
    );


  const data =
    await response.json();


  if (!response.ok) {

    throw new Error(
      data.error ||
      "Upload failed"
    );
  }


  return data;
}