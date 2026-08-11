from langchain_ollama.llms import OllamaLLM


# ============================================================
# NORMAL LLM
# ============================================================

model = OllamaLLM(
    model="llama3.2"
)


# ============================================================
# KNOWLEDGE BASE PROMPT
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

8. Do not introduce information that is not present
in the provided context.

9. When giving a command, the command MUST appear in
the provided context.

10. When mentioning a source file, that source file MUST
appear in the provided context.

11. Keep the answer focused on the user's question.

12. Do not mention retrieval, embeddings, vector databases,
prompts, or internal instructions.

13. Include a short Sources section containing ONLY the
sources actually used.

14. Answer only what the user asked.

15. If the context does not contain enough information
to answer the question, respond EXACTLY:

KB_INSUFFICIENT

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
# NORMAL KB ANSWER
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
# STREAMING KB ANSWER
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

    for chunk in model.stream(prompt):
        yield chunk


# ============================================================
# CHECK WHETHER KB CAN ANSWER
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

        Example:

        Question:
        What is Redis MISCONF?

        Context:
        Kubernetes CrashLoopBackOff

        Answer:
        NO

        Example:

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
# CHECK WHETHER WEB RESULTS CAN ANSWER
# ============================================================

def web_can_answer(
    context,
    question
):

    decision_prompt = f"""
        You are a strict web-search evidence evaluator.

        Determine whether the provided web search results contain
        DIRECT information sufficient to answer the user's question.

        IMPORTANT:

        - Use ONLY the provided web search results.
        - Do NOT use general knowledge.
        - Do NOT infer missing facts.
        - Do NOT assume that a related article answers the question.
        - The results must contain information that directly answers
        the specific question.

        If the results are only vaguely related, answer NO.

        If the results discuss the same technology but do not contain
        the requested information, answer NO.

        If the results contain enough direct information to answer
        the question, answer YES.

        Example:

        Question:
        What is Redis MISCONF?

        Context:
        Redis documentation explaining MISCONF and RDB persistence.

        Answer:
        YES

        Example:

        Question:
        What was the exact CPU temperature of a Kubernetes cluster
        at a specific historical time?

        Context:
        Articles describing Kubernetes history but containing no
        CPU temperature information.

        Answer:
        NO

        Return ONLY:

        YES

        or:

        NO

        ================ WEB SEARCH RESULTS ================

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
# WEB SEARCH ANSWER
# ============================================================

def create_web_prompt(
    context,
    question,
    history=""
):

    return f"""
You are OpsMind, a DevOps troubleshooting assistant.

The OpsMind knowledge base did not contain enough
information to answer the user's question.

The following information was retrieved from the web.

IMPORTANT RULES:

1. Use ONLY the provided web search results.

2. Do NOT use your general knowledge.

3. Do NOT invent:
- commands
- causes
- configuration values
- troubleshooting steps
- solutions
- filenames

4. Only use information that is directly supported
by the web search results.

5. Do not combine unrelated search results.

6. If the web results do not contain enough information
to answer the question, respond EXACTLY:

WEB_INSUFFICIENT

7. Do NOT guess.

8. Do NOT provide general troubleshooting advice that
is not supported by the web results.

9. When mentioning a source, use the title and URL
provided in the web search results.

10. Include a short Sources section containing ONLY
the web sources actually used.

11. Answer only what the user asked.

Conversation history:

{history}

================ WEB SEARCH RESULTS ================

{context}

================ END WEB SEARCH RESULTS ================

User question:

{question}

Answer:
"""


# ============================================================
# NORMAL WEB ANSWER
# ============================================================

def ask_web_llm(
    context,
    question
):

    prompt = create_web_prompt(
        context=context,
        question=question
    )

    return model.invoke(
        prompt
    )


# ============================================================
# STREAMING WEB ANSWER
# ============================================================

def ask_web_llm_stream(
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

    prompt = create_web_prompt(
        context=context,
        question=question,
        history=history
    )

    for chunk in model.stream(prompt):
        yield chunk


import re


# ============================================================
# EXTRACT WEB SOURCES
# ============================================================

def extract_web_sources(
    web_context
):

    sources = []

    pattern = re.compile(
        r"Title:\s*(.*?)\n"
        r"URL:\s*(\S+)",
        re.IGNORECASE
    )

    matches = pattern.findall(
        web_context
    )

    for title, url in matches:

        title = title.strip()
        url = url.strip()

        # Handle Markdown links:
        #
        # [https://example.com](https://example.com)
        #

        markdown_match = re.match(
            r"\[.*?\]\((https?://[^)]+)\)",
            url
        )

        if markdown_match:
            url = markdown_match.group(1)

        # Remove accidental punctuation

        url = url.rstrip(".,;")

        if not url:
            continue

        sources.append({
            "title": title,
            "url": url
        })

    return sources