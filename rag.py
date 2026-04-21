import json
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "knowledge.json")


def load_knowledge():
    with open(FILE_PATH, "r") as f:
        return json.load(f)

def retrieve_answer(query):
    data = load_knowledge()
    q = query.lower()
    if any(word in q for word in ["price", "pricing", "cost", "plan"]):
        return (
            f"Basic: {data['basic_plan']['price']} | "
            f"Pro: {data['pro_plan']['price']}"
        )

    if "basic" in q:
        return f"Basic Plan gives 10 videos/month at 720p for {data['basic_plan']['price']}."


    if "pro" in q:
         return f"Pro Plan gives unlimited videos, 4K, AI captions for {data['pro_plan']['price']}."

    if "refund" in q:
        return data["policies"]["refund"]

    if "support" in q:
        return data["policies"]["support"]

    return "Please ask about pricing, plans, features, refunds, or support."