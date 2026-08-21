from backend.state import ConversationMessage
from backend.llm import summarize_conversation


# ============================================================
# CONFIGURATION
# ============================================================

MAX_RECENT_MESSAGES = 6

# Once we have a full recent window, update the rolling summary.
SUMMARY_TRIGGER = MAX_RECENT_MESSAGES


# ============================================================
# MESSAGE MANAGEMENT
# ============================================================

def add_message(
    messages: list[ConversationMessage],
    role: str,
    content: str,
) -> list[ConversationMessage]:

    updated_messages = list(messages)

    updated_messages.append({
        "role": role,
        "content": content,
    })

    return updated_messages


# ============================================================
# RECENT MESSAGES
# ============================================================

def get_recent_messages(
    messages: list[ConversationMessage],
) -> list[ConversationMessage]:

    return messages[-MAX_RECENT_MESSAGES:]


# ============================================================
# SUMMARY
# ============================================================

def should_summarize(
    messages: list[ConversationMessage],
) -> bool:

    return len(messages) >= SUMMARY_TRIGGER


def update_summary(
    current_summary: str,
    messages: list[ConversationMessage],
) -> str:

    return summarize_conversation(
        current_summary=current_summary,
        messages=messages,
    )