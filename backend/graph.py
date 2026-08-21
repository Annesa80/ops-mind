from langgraph.graph import StateGraph, START, END

from backend.state import OpsMindState

from backend.hybrid_retriever import hybrid_search
from backend.reranker import rerank_documents

from backend.llm import (
    understand_query,
    kb_can_answer,
    web_can_answer,
    ask_llm_stream,
    ask_web_llm_stream,
    extract_web_sources,
)

from backend.conversation import (
    add_message,
    get_recent_messages,
    should_summarize,
    update_summary,
)

from backend.tools.web_search import web_search

from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()

from langgraph.config import get_stream_writer


# ============================================================
# CONFIGURATION
# ============================================================

RERANK_THRESHOLD = 0.1


def add_user_message(state: OpsMindState):

    recent_messages = list(
        state.get("recent_messages", [])
    )

    recent_messages = add_message(
        recent_messages,
        "user",
        state["question"],
    )

    return {
        "recent_messages": get_recent_messages(
            recent_messages
        )
    }

def add_assistant_message(state: OpsMindState):

    recent_messages = list(
        state.get("recent_messages", [])
    )

    recent_messages = add_message(
        recent_messages,
        "assistant",
        state["answer"],
    )

    return {
        "recent_messages": get_recent_messages(
            recent_messages
        )
    }

def update_conversation_summary(state: OpsMindState):

    recent_messages = state.get(
        "recent_messages",
        [],
    )

    if not should_summarize(
        recent_messages
    ):
        return {}

    summary = update_summary(
        state.get(
            "conversation_summary",
            "",
        ),
        recent_messages,
    )

    return {
        "conversation_summary": summary,
        "recent_messages": get_recent_messages(
            recent_messages
        ),
    }

# ============================================================
# NODE 1 — UNDERSTAND CONVERSATION
# ============================================================

def understand_conversation(state: OpsMindState):

    result = understand_query(
        summary=state.get(
            "conversation_summary",
            "",
        ),
        recent_messages=state.get(
            "recent_messages",
            [],
        ),
        question=state["question"],
    )

    print("\n================ OPSMIND QUERY =================")
    print("Original:", state["question"])
    print("Related:", result["related"])
    print("Retrieval:", result["query"])
    print("=================================================\n")

    return {
        "retrieval_query": result["query"],
        "conversation_related": result["related"],
    }


# ============================================================
# NODE 2 — RETRIEVE FROM KNOWLEDGE BASE
# ============================================================

def retrieve_kb(state: OpsMindState):

    retrieval_query = state["retrieval_query"]

    documents = hybrid_search(
        retrieval_query,
        dense_k=10,
        bm25_k=10,
        final_k=10,
    )

    return {
        "documents": documents
    }


# ============================================================
# NODE 3 — RERANK KNOWLEDGE BASE RESULTS
# ============================================================

def rerank_kb(state: OpsMindState):

    retrieval_query = state["retrieval_query"]
    documents = state["documents"]

    reranked_documents = rerank_documents(
        retrieval_query,
        documents,
        top_k=5,
    )

    context = "\n\n".join(
        f"Source: {document['metadata']['source']}\n"
        f"{document['text']}"
        for document in reranked_documents
    )

    sources = []
    seen = set()

    for document in reranked_documents:

        source = document["metadata"].get("source")

        if not source:
            continue

        if source in seen:
            continue

        seen.add(source)

        sources.append({
            "title": source,
            "url": None,
            "type": "kb",
        })

    return {
        "reranked_documents": reranked_documents,
        "context": context,
        "sources": sources,
    }


# ============================================================
# NODE 4 — CHECK RETRIEVAL QUALITY
# ============================================================

def check_retrieval_quality(state: OpsMindState):

    documents = state["reranked_documents"]

    if not documents:
        return {
            "retrieval_good": False
        }

    best_score = documents[0]["rerank_score"]

    return {
        "retrieval_good": (
            best_score >= RERANK_THRESHOLD
        )
    }


# ============================================================
# NODE 5 — CHECK WHETHER KB CAN ANSWER
# ============================================================

def evaluate_kb(state: OpsMindState):

    can_answer = kb_can_answer(
        context=state["context"],
        question=state["retrieval_query"],
    )

    return {
        "kb_can_answer": can_answer
    }


# ============================================================
# NODE 6 — ANSWER FROM KNOWLEDGE BASE
# ============================================================

def answer_from_kb(state: OpsMindState):

    writer = get_stream_writer()

    answer_parts = []

    for chunk in ask_llm_stream(
        context=state["context"],
        question=state["question"],
        conversation_summary=state.get(
            "conversation_summary",
            "",
        ),
        recent_messages=state.get(
            "recent_messages",
            [],
        ),
    ):

        text = str(chunk)

        answer_parts.append(text)

        writer({
            "type": "token",
            "content": text,
        })

    answer = "".join(answer_parts)

    # Send sources after the answer tokens
    writer({
        "type": "sources",
        "sources": state.get(
            "sources",
            [],
        ),
    })

    return {
        "answer": answer
    }


# ============================================================
# NODE 7 — SEARCH WEB
# ============================================================

def search_web(state: OpsMindState):

    retrieval_query = state["retrieval_query"]

    result = web_search.invoke({
        "query": retrieval_query
    })

    sources = extract_web_sources(result)

    return {
        "web_result": result,
        "sources": sources,
    }


# ============================================================
# NODE 8 — CHECK WHETHER WEB CAN ANSWER
# ============================================================

def evaluate_web(state: OpsMindState):

    can_answer = web_can_answer(
        context=state["web_result"],
        question=state["retrieval_query"],
    )

    return {
        "web_can_answer": can_answer
    }


# ============================================================
# NODE 9 — ANSWER FROM WEB
# ============================================================

def answer_from_web(state: OpsMindState):

    writer = get_stream_writer()

    answer_parts = []

    for chunk in ask_web_llm_stream(
        context=state["web_result"],
        question=state["question"],
        conversation_summary=state.get(
            "conversation_summary",
            "",
        ),
        recent_messages=state.get(
            "recent_messages",
            [],
        ),
    ):

        text = str(chunk)

        answer_parts.append(text)

        writer({
            "type": "token",
            "content": text,
        })

    answer = "".join(answer_parts)

    writer({
        "type": "sources",
        "sources": state.get(
            "sources",
            [],
        ),
    })

    return {
        "answer": answer
    }


# ============================================================
# NODE 10 — UNKNOWN ANSWER
# ============================================================

def answer_unknown(state: OpsMindState):

    writer = get_stream_writer()

    answer = (
        "I don't have enough information in the "
        "OpsMind knowledge base or the available web "
        "sources to answer this question."
    )

    writer({
        "type": "token",
        "content": answer,
    })

    writer({
        "type": "sources",
        "sources": state.get(
            "sources",
            [],
        ),
    })

    return {
        "answer": answer
    }


# ============================================================
# ROUTER — AFTER RETRIEVAL QUALITY
# ============================================================

def route_after_retrieval(state: OpsMindState):

    if state["retrieval_good"]:
        return "evaluate_kb"

    return "search_web"


# ============================================================
# ROUTER — AFTER KB EVALUATION
# ============================================================

def route_after_kb(state: OpsMindState):

    if state["kb_can_answer"]:
        return "answer_from_kb"

    return "search_web"


# ============================================================
# ROUTER — AFTER WEB EVALUATION
# ============================================================

def route_after_web(state: OpsMindState):

    if state["web_can_answer"]:
        return "answer_from_web"

    return "answer_unknown"


# ============================================================
# BUILD GRAPH
# ============================================================

builder = StateGraph(OpsMindState)


# ------------------------------------------------------------
# Add nodes
# ------------------------------------------------------------

builder.add_node(
    "understand_conversation",
    understand_conversation,
)
builder.add_node(
    "add_user_message",
    add_user_message,
)
builder.add_node(
    "add_assistant_message",
    add_assistant_message,
)

builder.add_node(
    "update_conversation_summary",
    update_conversation_summary,
)

builder.add_node(
    "retrieve_kb",
    retrieve_kb,
)

builder.add_node(
    "rerank_kb",
    rerank_kb,
)

builder.add_node(
    "check_retrieval_quality",
    check_retrieval_quality,
)

builder.add_node(
    "evaluate_kb",
    evaluate_kb,
)

builder.add_node(
    "answer_from_kb",
    answer_from_kb,
)

builder.add_node(
    "search_web",
    search_web,
)

builder.add_node(
    "evaluate_web",
    evaluate_web,
)

builder.add_node(
    "answer_from_web",
    answer_from_web,
)

builder.add_node(
    "answer_unknown",
    answer_unknown,
)


# ============================================================
# GRAPH FLOW
# ============================================================

builder.add_edge(
    START,
    "understand_conversation",
)

builder.add_edge(
    "understand_conversation",
    "add_user_message",
)

builder.add_edge(
    "add_user_message",
    "retrieve_kb",
)

builder.add_edge(
    "retrieve_kb",
    "rerank_kb",
)

builder.add_edge(
    "rerank_kb",
    "check_retrieval_quality",
)


# ============================================================
# RETRIEVAL ROUTING
# ============================================================

builder.add_conditional_edges(
    "check_retrieval_quality",
    route_after_retrieval,
    {
        "evaluate_kb": "evaluate_kb",
        "search_web": "search_web",
    },
)


# ============================================================
# KB ROUTING
# ============================================================

builder.add_conditional_edges(
    "evaluate_kb",
    route_after_kb,
    {
        "answer_from_kb": "answer_from_kb",
        "search_web": "search_web",
    },
)


# ============================================================
# WEB FLOW
# ============================================================

builder.add_edge(
    "search_web",
    "evaluate_web",
)


builder.add_conditional_edges(
    "evaluate_web",
    route_after_web,
    {
        "answer_from_web": "answer_from_web",
        "answer_unknown": "answer_unknown",
    },
)


# ============================================================
# END
# ============================================================

builder.add_edge(
    "answer_from_kb",
    "add_assistant_message",
)

builder.add_edge(
    "answer_from_web",
    "add_assistant_message",
)
builder.add_edge(
    "answer_unknown",
    "add_assistant_message",
)


builder.add_edge(
    "add_assistant_message",
    "update_conversation_summary",
)

builder.add_edge(
    "update_conversation_summary",
    END,
)


# ============================================================
# COMPILE
# ============================================================

graph = builder.compile(
    checkpointer=checkpointer
)



# ============================================================
# PUBLIC FUNCTION
# ============================================================

def run_opsmind(
    question: str,
    conversation_id: str,
):

    config = {
        "configurable": {
            "thread_id": conversation_id
        }
    }

    return graph.invoke(
        {
            "question": question,
        },
        config=config,
    )