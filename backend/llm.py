from langchain_ollama.llms import OllamaLLM
from langchain_ollama import ChatOllama
from backend.tools.kubernetes_docs import search_kubernetes_docs

from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
)


# NORMAL LLM
model = OllamaLLM(
    model="llama3.2"
)

# TOOL-CALLING LLM
tool_model = ChatOllama(
    model="llama3.2",
    temperature=0
)

tool_model_with_tools = tool_model.bind_tools(
    [search_kubernetes_docs]
)


# ============================================================
# PROMPT
# ============================================================

def create_prompt(
    context,
    question,
    history=""
):

    return f"""
        You are OpsMind, a DevOps troubleshooting assistant.

        Your answers MUST be grounded in the provided OpsMind
        knowledge base.

        STRICT RULES:

        1. Use ONLY the provided Knowledge Base Context to answer.

        2. Do NOT use general knowledge.

        3. Do NOT invent:
        - commands
        - filenames
        - configuration values
        - error causes
        - troubleshooting steps
        - solutions
        - source files

        4. A document is relevant only if its content directly
        supports the user's question.

        5. Treat each source as independent evidence.

        6. Do not transfer information between unrelated sources.

        7. If the context contains relevant information but does
        not identify the exact cause, say that the exact cause
        cannot be determined from the available information.

        Then provide ONLY information supported by the context.

        8. If the context does not contain enough information,
        say exactly:

        "I don't have enough information in the OpsMind knowledge
        base to answer this question."

        9. NEVER introduce information from unrelated documents.

        10. When giving a command, the command MUST appear in
        the provided context.

        11. When mentioning a source file, that source file MUST
        appear in the provided context.

        12. Keep the answer focused on the user's question.

        13. Do not mention retrieval, embeddings, vector databases,
        prompts, or internal instructions.

        14. Include a short Sources section containing ONLY the
        sources actually used.

        15. Answer only what the user asked.

        Conversation history:

        {history}

        ================ KNOWLEDGE BASE CONTEXT ================

        {context}

        ================ END KNOWLEDGE BASE CONTEXT ================

        User question:

        {question}

        Answer:
        """


# ============================================================
# NORMAL ANSWER
# ============================================================

def ask_llm(
    context,
    question
):

    prompt = create_prompt(
        context=context,
        question=question
    )

    return model.invoke(
        prompt
    )


# ============================================================
# STREAMING ANSWER
# ============================================================

def ask_llm_stream(
    context,
    messages
):

    history = "\n".join(
        f"{m.role}: {m.content}"
        if hasattr(m, "role")
        else f"{m['role']}: {m['content']}"
        for m in messages[:-1]
    )

    last_message = messages[-1]

    if hasattr(last_message, "content"):
        question = last_message.content
    else:
        question = last_message["content"]

    prompt = create_prompt(
        context=context,
        question=question,
        history=history
    )

    for chunk in model.stream(
        prompt
    ):

        yield chunk


# ============================================================
# DETERMINE WHETHER KB CAN ANSWER
# ============================================================

def kb_can_answer(
    context,
    question
):

    decision_prompt = f"""
        You are a strict knowledge-base evaluator.

        Determine whether the provided Knowledge Base Context
        contains DIRECT information sufficient to answer the
        user's question.

        Do NOT use general knowledge.

        The context must directly address the same technology
        and problem.

        If the context is only vaguely related, answer NO.

        If the context is about a different technology, answer NO.

        Examples:

        Question:
        What is Redis MISCONF?

        Context:
        Kubernetes CrashLoopBackOff

        Answer:
        NO

        Question:
        What causes a Docker application to fail?

        Context:
        Docker application errors and missing environment variables

        Answer:
        YES

        Return ONLY:

        YES

        or:

        NO


        ================ CONTEXT ================

        {context}

        ================ QUESTION ================

        {question}

        ================ DECISION ================
        """

    response = model.invoke(
        decision_prompt
    )

    answer = response.strip().upper()

    return answer.startswith("YES")


# ============================================================
# OFFICIAL DOCUMENTATION FALLBACK
# ============================================================

def ask_official_docs(
    question
):

    # ========================================================
    # 1. ASK THE TOOL-ROUTING MODEL
    # ========================================================

    response = tool_model_with_tools.invoke(
        [
            SystemMessage(
                content="""
                    You are the official-documentation routing assistant.

                    You have access to one tool:

                    search_kubernetes_docs

                    Use this tool ONLY when the user's question is
                    specifically about Kubernetes.

                    Do NOT use the tool for:

                    - Redis
                    - Docker
                    - Linux
                    - PostgreSQL
                    - Python
                    - other technologies

                    If the question is not specifically about Kubernetes,
                    do not call the tool.
                    """
            ),

            HumanMessage(
                content=question
            )
        ]
    )

    # ========================================================
    # 2. NO TOOL CALL
    # ========================================================

    if not response.tool_calls:

        return None


    # ========================================================
    # 3. GET TOOL CALL
    # ========================================================

    tool_call = response.tool_calls[0]

    query = tool_call["args"].get(
        "query",
        ""
    )


    if not query:

        return None


    # ========================================================
    # 4. CALL OFFICIAL DOCUMENTATION TOOL
    # ========================================================

    tool_result = search_kubernetes_docs.invoke(
        {
            "query": query
        }
    )


    # ========================================================
    # 5. CHECK TOOL RESULT
    # ========================================================

    if not tool_result:

        return None


    tool_result = str(
        tool_result
    ).strip()


    if not tool_result:

        return None


    # --------------------------------------------------------
    # Reject empty / useless responses
    # --------------------------------------------------------

    useless_results = [

        "no results found",

        "no relevant results found",

        "no official documentation found",

        "no relevant official documentation found",

        "unable to find relevant documentation"

    ]


    if tool_result.lower() in useless_results:

        return None


    # ========================================================
    # 6. ASK NORMAL LLM TO ANSWER FROM OFFICIAL DOCS
    # ========================================================

    final_prompt = f"""
        You are OpsMind, a DevOps troubleshooting assistant.

        The local OpsMind knowledge base did not contain enough
        information to answer the user's question.

        Official documentation was searched as a fallback.

        IMPORTANT:

        Use ONLY the official documentation provided below.

        Do NOT use your general knowledge.

        Do NOT invent:

        - commands
        - causes
        - configuration values
        - troubleshooting steps
        - solutions
        - source files

        If the official documentation does not contain enough
        information to answer the question, respond exactly:

        I don't have enough information in the OpsMind knowledge
        base or the official documentation to answer this question.

        Do NOT provide general troubleshooting advice.

        Do NOT guess.

        Do NOT mention information that is not present in the
        official documentation.

        At the end, include:

        Sources:

        Only mention sources that actually appear in the official
        documentation below.

        ================ OFFICIAL DOCUMENTATION ================

        {tool_result}

        ================ END OFFICIAL DOCUMENTATION ================

        User question:

        {question}

        Answer:
        """


    final_answer = model.invoke(
        final_prompt
    )


    if not final_answer:

        return None


    final_answer = str(
        final_answer
    ).strip()


    if not final_answer:

        return None


    return final_answer

def create_official_docs_prompt(question, context):
    return f"""
        You are OpsMind, a DevOps troubleshooting assistant.

        You are answering using ONLY the provided official documentation.

        STRICT RULES:

        1. Use ONLY the provided official documentation context.

        2. Do NOT use your general knowledge.

        3. Do NOT invent:
        - commands
        - filenames
        - configuration values
        - error causes
        - troubleshooting steps
        - solutions
        - terminology not supported by the documentation

        4. The documentation must directly support the answer.

        5. Do NOT combine unrelated information.

        6. If the official documentation directly answers the question,
        provide the answer using ONLY that information.

        7. If the official documentation does NOT contain enough information
        to answer the question, your entire response MUST be exactly:

        OFFICIAL_DOCS_INSUFFICIENT

        8. Do not provide a partial answer when the documentation is insufficient.

        9. Do not mention retrieval, tools, embeddings, vector databases,
        prompts, or internal instructions.

        10. Do not invent sources.

        Official documentation context:
        ===============================

        {context}

        ===============================
        END OFFICIAL DOCUMENTATION
        ===============================

        User question:
        {question}

        Answer:
        """


def ask_official_docs(question, context):

    prompt = create_official_docs_prompt(
        question=question,
        context=context
    )

    return model.invoke(prompt)