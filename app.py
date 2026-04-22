import json

from mock_tool import mock_lead_capture

with open("rag_data.json", encoding="utf-8") as f:
    knowledge = json.load(f)

memory = {
    "intent": None,
    "selected_plan": None,
    "lead_stage": None,
    "name": None,
    "email": None,
    "platform": None,
}


def has_any_term(text, terms):
    return any(term in text for term in terms)


def detect_intent(user_input):
    user_input = user_input.lower().strip()
    has_greeting = has_any_term(user_input, ["hi", "hello", "hey"])
    has_high_intent = has_any_term(
        user_input,
        [
            "i want pro",
            "pro plan",
            "buy",
            "subscribe",
            "sign up",
            "get started",
            "try pro",
        ],
    )
    has_pricing = has_any_term(user_input, ["price", "pricing", "cost", "plan"])

    if has_greeting and has_pricing:
        return "greeting_pricing"
    if has_greeting:
        return "greeting"
    if has_high_intent:
        return "high_intent"
    if has_pricing:
        return "pricing"
    return "general"


def get_plan_details(plan_name):
    plan = knowledge["pricing"][plan_name]
    return (
        f"The {plan_name.title()} plan includes:\n"
        + "\n".join(f"- {feature}" for feature in plan["features"])
    )


def get_pricing():
    basic = knowledge["pricing"]["basic"]
    pro = knowledge["pricing"]["pro"]
    return (
        "AutoStream Pricing:\n"
        f"Basic Plan: {basic['price']}\n"
        f"Features: {', '.join(basic['features'])}\n\n"
        f"Pro Plan: {pro['price']}\n"
        f"Features: {', '.join(pro['features'])}"
    )


def handle_lead_capture(user_input):
    if memory["lead_stage"] == "ask_name":
        memory["name"] = user_input.strip()
        memory["lead_stage"] = "ask_email"
        print("Agent: Please provide your email.")
        return True

    if memory["lead_stage"] == "ask_email":
        memory["email"] = user_input.strip()
        memory["lead_stage"] = "ask_platform"
        print("Agent: Which platform do you create content on? (YouTube, Instagram etc.)")
        return True

    if memory["lead_stage"] == "ask_platform":
        memory["platform"] = user_input.strip()
        memory["lead_stage"] = None
        mock_lead_capture(memory["name"], memory["email"], memory["platform"])
        return True

    return False


while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        break

    if handle_lead_capture(user_input):
        continue

    intent = detect_intent(user_input)
    memory["intent"] = intent

    if intent == "greeting_pricing":
        print("Agent: Hello! I can help you with AutoStream pricing and features.")
        print(get_pricing())
    elif intent == "greeting":
        print("Agent: Hello! I can help you with AutoStream pricing and features.")
    elif intent == "pricing":
        print("Agent: Here are the pricing details for AutoStream:")
        print(get_pricing())
    elif intent == "high_intent":
        memory["selected_plan"] = "pro" if "pro" in user_input.lower() else None
        if memory["selected_plan"] == "pro":
            print("Agent: Great choice! " + get_plan_details("pro"))
        else:
            print("Agent: Great! I can help you get started.")
        memory["lead_stage"] = "ask_name"
        print("Agent: May I know your name?")
    else:
        print("Agent: I can help with pricing or help you get started with a plan.")
