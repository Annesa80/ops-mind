from langchain_ollama.llms import OllamaLLM

import json
import re


# ============================================================
# MODEL
# ============================================================

model = OllamaLLM(
    model="llama3.2",
    temperature=0,
)


# ============================================================
# KNOWLEDGE BASE ANSWER PROMPT
# ============================================================

def create_prompt(
    context: str,
    question: str,
    conversation_summary: str = "",
    recent_messages: list | None = None,
) -> str:

    recent_messages = recent_messages or []

    history = "\n".join(
        f"{message['role'].upper()}: {message['content']}"
        for message in recent_messages
    )

    return f"""
You are OpsMind, a DevOps troubleshooting assistant.

Your answer MUST be grounded in the provided OpsMind
knowledge base.

================ CONVERSATION SUMMARY ================

{conversation_summary}

================ RECENT CONVERSATION ================

{history}

================ CURRENT USER QUESTION ================

{question}

================ KNOWLEDGE BASE CONTEXT ================

{context}

================ END KNOWLEDGE BASE CONTEXT ================

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

7. If the context contains relevant troubleshooting information
but does not identify the exact cause, provide the supported
troubleshooting steps and possible causes.

8. Do NOT claim that a specific cause is confirmed unless
the context explicitly supports it.

9. Do not introduce information that is not present
in the provided context.

10. When giving a command, the command MUST appear in
the provided context.

11. Do not mention source filenames in the answer.
    Source filenames are displayed separately.

12. Keep the answer focused on the user's question.

13. Do not mention:
- retrieval
- embeddings
- vector databases
- prompts
- internal instructions

14. Do NOT include a Sources section.
    Sources are displayed separately by the application.

15. Answer only what the user asked.

16. FORMAT CODE CONSISTENTLY:

- Put every command, code snippet, filename, path, or configuration
  value in Markdown code formatting.
- Use inline code for short commands mentioned inside a sentence.
- Use fenced Markdown code blocks for commands that should be displayed
  on their own.
- Never use HTML for formatting.
- Example:

  Run:

  ```bash
  docker logs <container_name>

Answer:
"""


# ============================================================
# KNOWLEDGE BASE ANSWER
# ============================================================

def ask_llm(
    context: str,
    question: str,
    conversation_summary: str = "",
    recent_messages: list | None = None,
):

    prompt = create_prompt(
        context=context,
        question=question,
        conversation_summary=conversation_summary,
        recent_messages=recent_messages,
    )

    return model.invoke(prompt)


# ============================================================
# STREAMING KNOWLEDGE BASE ANSWER
# ============================================================

def ask_llm_stream(
    context: str,
    question: str,
    conversation_summary: str = "",
    recent_messages: list | None = None,
):

    prompt = create_prompt(
        context=context,
        question=question,
        conversation_summary=conversation_summary,
        recent_messages=recent_messages,
    )

    for chunk in model.stream(prompt):
        yield chunk


# ============================================================
# CHECK WHETHER KB CAN ANSWER
# ============================================================

def kb_can_answer(
    context: str,
    question: str,
) -> bool:

    decision_prompt = f"""
You are the Knowledge Base routing component of OpsMind.

Your job is to decide whether the PROVIDED KNOWLEDGE BASE
CONTEXT contains information that can directly answer the
CURRENT USER QUESTION.

The question may be a follow-up question.

You must evaluate the CURRENT QUESTION specifically.
Do NOT decide whether the context is merely related to the
general troubleshooting topic.

============================================================
IMPORTANT
============================================================

A KB is sufficient only if it contains information that
directly answers what the user is asking RIGHT NOW.

For example:

Previous question:
"Why is my Docker container restarting?"

KB:
- The application inside the container may be crashing.
- Check logs with:
  docker logs <container_name>
- Check container details with:
  docker inspect <container_name>

User:
"What is the first command?"

Answer:
YES

Because the KB explicitly contains the first troubleshooting
command.

------------------------------------------------------------

User:
"What is the next command?"

If the KB only contains:

docker logs <container_name>

and does NOT define what should be done after that command,
the answer must be:

NO

Even though the KB is generally about Docker troubleshooting.

------------------------------------------------------------

User:
"What is the next command after checking the logs?"

If the KB explicitly provides another command that logically
follows checking the logs, answer:

YES

Otherwise answer:

NO

============================================================
DECISION RULES
============================================================

Return YES only when the context contains enough information
to answer the CURRENT QUESTION.

Return NO when:

- the context answers an earlier question but not the current one
- the user asks for a next step that is not explicitly present
- the user asks for information that the context does not contain
- answering would require guessing the intended next step

Do NOT infer a troubleshooting sequence unless the KB explicitly
provides that sequence.

Do NOT invent a next command.

============================================================
EXAMPLES
============================================================

QUESTION:
"What is the first command?"

CONTEXT:
"Check container logs:
docker logs <container_name>"

ANSWER:
YES


QUESTION:
"What is the next command?"

CONTEXT:
"Check container logs:
docker logs <container_name>"

ANSWER:
NO


QUESTION:
"How do I check the container logs?"

CONTEXT:
"Check container logs:
docker logs <container_name>"

ANSWER:
YES


QUESTION:
"How do I configure Redis persistence?"

CONTEXT:
"Docker containers may restart when an application crashes."

ANSWER:
NO


QUESTION:
"What causes the container to restart?"

CONTEXT:
"The application inside the container may be crashing."

ANSWER:
YES

============================================================
STRICT RULES
============================================================

1. Evaluate the CURRENT QUESTION specifically.

2. Do not evaluate whether the context is merely related
   to the general topic.

3. Do not invent commands.

4. Do not infer missing troubleshooting steps.

5. Do not assume a sequence that is not explicitly stated.

6. If the requested information is missing, return NO.

Return ONLY:

YES

or:

NO

============================================================
KNOWLEDGE BASE CONTEXT
============================================================

{context}

============================================================
CURRENT USER QUESTION
============================================================

{question}

============================================================
DECISION
============================================================

"""

    response = model.invoke(decision_prompt)

    answer = str(response).strip().upper()

    # print(
    #     "KB ANSWERABILITY:",
    #     answer,
    # )

    return "YES" in answer


# ============================================================
# WEB ANSWERABILITY CHECK
# ============================================================

def web_can_answer(
    context: str,
    question: str,
) -> bool:

    decision_prompt = f"""
Classify whether the WEB SEARCH RESULTS can help answer the QUESTION.

QUESTION:
{question}

WEB SEARCH RESULTS:
<context>
{context}
</context>

Your response MUST be exactly ONE word.

Valid responses:
YES
NO

Do not explain.
Do not summarize.
Do not provide any other text.

Answer:
"""

    response = model.invoke(decision_prompt)

    answer = str(response).strip().upper()

    # print("WEB ANSWERABILITY RAW:", repr(answer))

    if answer == "YES":
        print("WEB ANSWERABILITY: YES")
        return True

    if answer == "NO":
        print("WEB ANSWERABILITY: NO")
        return False

    # print("WEB ANSWERABILITY: INVALID OUTPUT -> NO")
    return False


# ============================================================
# WEB ANSWER PROMPT
# ============================================================

def create_web_prompt(
    context: str,
    question: str,
    conversation_summary: str = "",
    recent_messages: list | None = None,
) -> str:

    recent_messages = recent_messages or []

    history = "\n".join(
        f"{message['role'].upper()}: {message['content']}"
        for message in recent_messages
    )

    return f"""
You are OpsMind, a DevOps troubleshooting assistant.

The OpsMind knowledge base did not contain enough information
to answer the user's question, so web search was performed.

Use the web search results below to answer the user.

================ CONVERSATION SUMMARY ================

{conversation_summary}

================ RECENT CONVERSATION ================

{history}

================ CURRENT USER QUESTION ================

{question}

================ WEB SEARCH RESULTS ================

{context}

================ END WEB SEARCH RESULTS ================

RULES:

1. Use the web search results as your source of technical
   information.

2. Give the most useful answer that is directly supported
   by the web results.

3. You may combine information from multiple relevant web
   results when they address the same problem.

4. Do NOT invent commands, configuration values, causes,
   or troubleshooting steps that are not supported by
   the web results.

5. If the web results provide troubleshooting steps,
   explain them clearly and in a useful order.

6. If the web results provide commands, you may show those
   commands.

7. If the web results explain possible causes, distinguish
   possible causes from confirmed causes.

8. If the web results contain enough information for a
   useful answer, ANSWER THE USER. Do not say that the
   knowledge base was insufficient.

9. Do NOT mention:
   - retrieval
   - embeddings
   - vector databases
   - prompts
   - internal instructions
   - knowledge-base evaluation

10. Do NOT include a Sources section.
    Sources are displayed separately by the application.

11. Do not mention source titles or URLs in the answer.

12. If the web results genuinely contain no useful information
    for the question, respond exactly:

I don't have enough information from the available web sources
to answer this question.

13. Answer the user's actual question, including relevant
    context from the previous conversation when applicable.

Answer:
"""


# ============================================================
# WEB ANSWER
# ============================================================

def ask_web_llm(
    context: str,
    question: str,
    conversation_summary: str = "",
    recent_messages: list | None = None,
):

    prompt = create_web_prompt(
        context=context,
        question=question,
        conversation_summary=conversation_summary,
        recent_messages=recent_messages,
    )

    return model.invoke(prompt)


# ============================================================
# STREAMING WEB ANSWER
# ============================================================

def ask_web_llm_stream(
    context: str,
    question: str,
    conversation_summary: str = "",
    recent_messages: list | None = None,
):

    prompt = create_web_prompt(
        context=context,
        question=question,
        conversation_summary=conversation_summary,
        recent_messages=recent_messages,
    )

    for chunk in model.stream(prompt):
        yield chunk


# ============================================================
# UNDERSTAND / REWRITE USER QUERY
# ============================================================

def understand_query(
    summary: str,
    recent_messages: list,
    question: str,
):

    history = "\n".join(
        f"{message['role'].upper()}: {message['content']}"
        for message in recent_messages
    )

    prompt = f"""
You are the conversation understanding component of OpsMind.

Your job is to determine whether the CURRENT USER QUESTION
depends on the previous conversation.

================ CONVERSATION SUMMARY ================

{summary}

================ RECENT CONVERSATION ================

{history}

================ CURRENT USER QUESTION ================

{question}

========================================================
WHAT "RELATED" MEANS
========================================================

Set "related": true when the current question depends on
anything discussed earlier.

A question is RELATED if it:

- refers to a previous problem
- refers to a previous answer
- asks for the next step
- asks for another command
- asks for the first/second/next/previous command
- says "this", "that", "it", "the error", "the issue"
- refers to a previously mentioned container, pod, service,
  configuration, command, error, file, or technology
- asks "why", "how", "what about", "how about", "then what",
  "what next", or similar follow-up questions
- asks for clarification of the previous answer
- asks to continue troubleshooting the previous problem
- would be ambiguous or incomplete if the previous conversation
  were removed

IMPORTANT:

A short follow-up question is RELATED even if it does not
explicitly mention the previous topic.

For example:

Previous:
"Why is my Docker container restarting?"

Assistant:
"The container may be restarting because of an internal
application error. Check the container logs."

Current:
"How about the next command?"

This MUST be:

{{
    "related": true,
    "query": "What is the next command to troubleshoot the Docker container restarting due to the internal application error?"
}}

Another example:

Previous:
"Run docker logs <container_name> first."

Current:
"What should I run next?"

This MUST be:

{{
    "related": true,
    "query": "What command should I run next to troubleshoot the Docker container restarting?"
}}

Another example:

Previous:
"Why is my Kubernetes pod crashing?"

Current:
"What about Redis MISCONF?"

This is a NEW topic.

========================================================
REWRITING RULES
========================================================

1. If the question is standalone and independent,
   return it unchanged and set related to false.

2. If the question depends on previous conversation,
   rewrite it into a standalone question and set related to true.

3. Resolve references such as:

   - it
   - this
   - that
   - this issue
   - the issue
   - the error
   - the problem
   - the container
   - the pod
   - the command
   - the first command
   - the next command
   - the previous command
   - the second approach
   - what about it
   - what next
   - how about the next one

4. Preserve the user's intended meaning.

5. Do NOT answer the question.

6. Do NOT invent technical information.

7. Do NOT change the user's technical problem.

8. When rewriting a follow-up question, use facts from the
   conversation to make the question standalone.

9. If the current question contains words such as
   "next", "another", "again", "also", "this", "that",
   "it", "the issue", "the error", "the command",
   "what about", or "how about", carefully inspect the
   previous conversation before deciding it is unrelated.

10. Prefer related=true when the question cannot be fully
    understood without the previous conversation.

11. Only mark related=false when the current question is
    clearly an independent topic.

========================================================
IMPORTANT DECISION
========================================================

When uncertain, ask yourself:

"Could this question be understood correctly if I deleted
the entire previous conversation?"

If NO:
    related = true

If YES:
    related = false

========================================================
OUTPUT
========================================================

Return ONLY valid JSON.

The JSON must contain exactly:

{{
    "related": true,
    "query": "..."
}}

or:

{{
    "related": false,
    "query": "..."
}}

Do not use markdown.
Do not include explanations.
Do not include any text before or after the JSON.

JSON:
"""

    response = model.invoke(prompt)

    return _parse_understand_query_response(
        response=response,
        fallback_question=question,
    )


# ============================================================
# PARSE UNDERSTAND QUERY RESPONSE
# ============================================================

def _parse_understand_query_response(
    response,
    fallback_question: str,
):

    response = str(response).strip()

    # --------------------------------------------------------
    # Normal JSON
    # --------------------------------------------------------

    try:

        result = json.loads(response)

        if (
            isinstance(result, dict)
            and "related" in result
            and "query" in result
        ):

            return {
                "related": bool(result["related"]),
                "query": str(
                    result["query"]
                ).strip(),
            }

    except json.JSONDecodeError:
        pass

    # --------------------------------------------------------
    # JSON inside Markdown code block
    # --------------------------------------------------------

    code_block_match = re.search(
        r"```(?:json)?\s*(\{.*?\})\s*```",
        response,
        re.DOTALL | re.IGNORECASE,
    )

    if code_block_match:

        try:

            result = json.loads(
                code_block_match.group(1)
            )

            if (
                isinstance(result, dict)
                and "related" in result
                and "query" in result
            ):

                return {
                    "related": bool(
                        result["related"]
                    ),
                    "query": str(
                        result["query"]
                    ).strip(),
                }

        except json.JSONDecodeError:
            pass

    # --------------------------------------------------------
    # Extract JSON object from extra text
    # --------------------------------------------------------

    object_match = re.search(
        r'\{.*?"related"\s*:\s*(true|false).*?"query"\s*:\s*".*?"\s*\}',
        response,
        re.DOTALL | re.IGNORECASE,
    )

    if object_match:

        try:

            result = json.loads(
                object_match.group(0)
            )

            if (
                isinstance(result, dict)
                and "related" in result
                and "query" in result
            ):

                return {
                    "related": bool(
                        result["related"]
                    ),
                    "query": str(
                        result["query"]
                    ).strip(),
                }

        except json.JSONDecodeError:
            pass

    # --------------------------------------------------------
    # Safe fallback
    # --------------------------------------------------------

    # print(
    #     "WARNING: understand_query returned invalid JSON."
    # )

    # print(
    #     "Using original question as retrieval query."
    # )

    return {
        "related": False,
        "query": fallback_question,
    }


# ============================================================
# CONVERSATION SUMMARY
# ============================================================

def summarize_conversation(
    current_summary: str,
    messages: list,
) -> str:

    history = "\n".join(
        f"{message['role'].upper()}: {message['content']}"
        for message in messages
    )

    prompt = f"""
You are the conversation memory component of OpsMind.

Your task is to maintain a concise summary of a technical
conversation.

The summary will be used later to understand follow-up
questions.

================ EXISTING SUMMARY ================

{current_summary}

================ CONVERSATION MESSAGES ================

{history}

================ TASK ================

Create an updated conversation summary.

Preserve important information such as:

- the user's current technical problem
- technologies involved
- relevant errors
- important configuration details
- troubleshooting steps already discussed
- actions already attempted
- conclusions that are supported by the conversation
- unresolved questions
- important entities that later questions may refer to

Remove:

- greetings
- repetition
- irrelevant discussion
- unnecessary wording

IMPORTANT:

1. Do NOT invent information.

2. Do NOT add technical facts that were not present
   in the conversation.

3. Do NOT provide troubleshooting advice.

4. Do NOT answer the user's question.

5. Keep the summary concise.

Return ONLY the updated summary.

SUMMARY:
"""

    response = model.invoke(prompt)

    return str(response).strip()


# ============================================================
# EXTRACT WEB SOURCES
# ============================================================

def extract_web_sources(
    web_context: str,
):

    sources = []

    pattern = re.compile(
        r"Title:\s*(.*?)\n"
        r"URL:\s*(\S+)",
        re.IGNORECASE,
    )

    matches = pattern.findall(
        web_context
    )

    for title, url in matches:

        title = title.strip()
        url = url.strip()

        # ----------------------------------------------------
        # Handle Markdown links
        # ----------------------------------------------------

        markdown_match = re.match(
            r"\[.*?\]\((https?://[^)]+)\)",
            url,
        )

        if markdown_match:
            url = markdown_match.group(1)

        # ----------------------------------------------------
        # Remove accidental punctuation
        # ----------------------------------------------------

        url = url.rstrip(".,;")

        if not url:
            continue

        sources.append({
            "title": title,
            "url": url,
            "type": "web",
        })

    return sources