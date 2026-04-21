def detect_intent(user_input):
    text = user_input.lower().strip()

    high_intent_keywords = [
        "i want", "buy", "subscribe", "sign up",
        "trial", "try pro", "get started",
        "need this", "use this for", "interested"
    ]

    product_keywords = [
        "price", "pricing", "cost", "plan", "plans",
        "feature", "features", "refund", "support",
        "pro", "basic", "4k", "videos"
    ]

    greeting_keywords = ["hi", "hello", "hey"]

    if any(k in text for k in high_intent_keywords):
        return "high_intent"

    if any(k in text for k in product_keywords):
        return "product_query"

    if any(k == text for k in greeting_keywords):
        return "greeting"

    return "unknown"