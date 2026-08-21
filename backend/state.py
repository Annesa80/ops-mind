from typing import TypedDict


class ConversationMessage(TypedDict):
    role: str
    content: str


class OpsMindState(TypedDict, total=False):

    # ========================================================
    # CONVERSATION
    # ========================================================

    question: str

    conversation_summary: str

    # We keep the bounded recent conversation in graph state.
    # The LLM will only receive these recent messages.
    recent_messages: list[ConversationMessage]

    # ========================================================
    # QUERY UNDERSTANDING
    # ========================================================

    retrieval_query: str
    conversation_related: bool

    # ========================================================
    # KNOWLEDGE BASE
    # ========================================================

    documents: list
    reranked_documents: list

    context: str

    sources: list

    retrieval_good: bool
    kb_can_answer: bool

    # ========================================================
    # WEB
    # ========================================================

    web_result: object
    web_can_answer: bool

    # ========================================================
    # ANSWER
    # ========================================================

    answer: str