# app.py
from typing import TypedDict
from langgraph.graph import StateGraph, END

from intent import detect_intent
from rag import retrieve_answer
from tools import mock_lead_capture


class AgentState(TypedDict):
    user_input: str
    intent: str
    response: str
    name: str
    email: str
    platform: str
    awaiting_field: str
    lead_done: bool


def classify_node(state):
    # If already collecting lead details, stay in lead flow
    if state["intent"]:
        return state
    if state["awaiting_field"]:
        state["intent"] = "high_intent"
        return state

    state["intent"] = detect_intent(state["user_input"])
    return state



def greeting_node(state):
    state["response"] = "Hello! Welcome to AutoStream. How can I help you?"
    return state



def product_node(state):
    state["response"] = retrieve_answer(state["user_input"])
    return state



def unknown_node(state):
    state["response"] = (
        "I can help with AutoStream pricing, plans, features, or sign-up."
    )
    return state


def lead_node(state):
    if state["lead_done"]:
        state["response"] = "Your lead is already captured. Our team will contact you soon."
        return state


    if not state["name"]:
        state["response"] = "Great! What's your name?"
        state["awaiting_field"] = "name"
        return state
    if not state["email"]:
        state["response"] = "Please share your email."
        state["awaiting_field"] = "email"
        return state
    if not state["platform"]:
        state["response"] = "Which creator platform do you use? (YouTube / Instagram / etc.)"
        state["awaiting_field"] = "platform"
        return state

    mock_lead_capture(state["name"], state["email"], state["platform"])

    state["response"] = "Thanks! Your lead has been captured successfully."
    state["awaiting_field"] = ""
    state["lead_done"] = True
    return state


def router(state):
    return state["intent"]


graph = StateGraph(AgentState)

graph.add_node("classify", classify_node)
graph.add_node("greeting", greeting_node)
graph.add_node("product_query", product_node)
graph.add_node("high_intent", lead_node)
graph.add_node("unknown", unknown_node)

graph.set_entry_point("classify")

graph.add_conditional_edges(
    "classify",
    router,
    {
        "greeting": "greeting",
        "product_query": "product_query",
        "high_intent": "high_intent",
        "unknown": "unknown",
    },
)

graph.add_edge("greeting", END)
graph.add_edge("product_query", END)
graph.add_edge("high_intent", END)
graph.add_edge("unknown", END)

app = graph.compile()


memory = {
    "name": "",
    "email": "",
    "platform": "",
    "awaiting_field": "",
    "lead_done": False
}


print("Type 'exit' to quit.\n")

while True:
    user = input("You: ").strip()

    if user.lower() == "exit":
        break
    
    forced_intent = ""

    if memory["awaiting_field"] == "name":
        memory["name"] = user
        memory["awaiting_field"] = ""
        forced_intent = "high_intent"

    elif memory["awaiting_field"] == "email":
        memory["email"] = user
        memory["awaiting_field"] = ""
        forced_intent = "high_intent"

    elif memory["awaiting_field"] == "platform":
        memory["platform"] = user
        memory["awaiting_field"] = ""
        forced_intent = "high_intent"

    result = app.invoke({
        "user_input": user,
        "intent": forced_intent,
        "response": "",
        "name": memory["name"],
        "email": memory["email"],
        "platform": memory["platform"],
        "awaiting_field": memory["awaiting_field"],
        "lead_done": memory["lead_done"]
    })

    memory["awaiting_field"] = result["awaiting_field"]
    memory["lead_done"] = result["lead_done"]
    
    

    print("Bot:", result["response"])