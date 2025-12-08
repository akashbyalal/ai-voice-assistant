def get_intent(text):
    text = text.lower()

    if "what is" in text:
        return "query"
    if "define" in text:
        return "query"
    if "formula" in text:
        return "query"
    if "explain" in text:
        return "query"

    return "unknown"
