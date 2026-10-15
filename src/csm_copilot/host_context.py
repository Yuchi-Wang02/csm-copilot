"""Optional final-request reduction using host-owned message positions, never text search."""

from copy import deepcopy


def compact_final_messages(messages, policy_message_indexes):
    """Retain all content except earlier host policy messages; preserve an omission audit."""
    indexes = policy_message_indexes
    if (
        not indexes
        or any(type(index) is not int or not 0 <= index < len(messages) for index in indexes)
        or indexes != sorted(set(indexes))
    ):
        raise ValueError("Expected distinct, ordered positions for host policy messages")
    for index in indexes:
        message = messages[index]
        if message.get("role") != "user" or not isinstance(message.get("content"), str):
            raise ValueError("Tracked host policy position has an invalid message")
        if not message["content"].startswith("Host workflow policy (not customer data): "):
            raise ValueError("Tracked host policy position does not identify a policy message")
    removed = set(indexes[:-1])
    retained = [index for index in range(len(messages)) if index not in removed]
    audit = {
        "method": "superseded_policy_messages_v1",
        "original_message_count": len(messages),
        "retained_message_count": len(retained),
        "retained_message_indexes": retained,
        "omitted_messages": [
            {"original_index": index, "message": deepcopy(messages[index])}
            for index in indexes[:-1]
        ],
        "boundary": "Only earlier host-generated policy messages are omitted from this worker request. The latest policy, initial instructions, task, model responses, tool-result messages, final contracts and correction feedback are retained. The full history remains reconstructable. This changes model input; it does not establish a speed or answer-quality improvement.",
    }
    return [deepcopy(messages[index]) for index in retained], audit
