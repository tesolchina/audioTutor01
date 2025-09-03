import json
import requests
from flask import Blueprint, jsonify, request

# ------------------------------
# Blueprint (REST endpoint)
# ------------------------------
chatbot = Blueprint("chatbot", __name__)


@chatbot.route("/a", methods=["GET"])
def hello_module1():
    return jsonify({"message": "Hello from Module chatbot"})


# --- Simplified Preprocess Function ---
def preprocess_chat_history(chat_history):
    """
    Convert chat history into the plain format expected by HKBU API:
    [
      {"role": "system", "content": "..."},
      {"role": "user", "content": "..."}
    ]
    """
    processed = []
    first_assistant_removed = False

    for msg in chat_history:
        role = msg.get("role")
        content = msg.get("content")

        if not content:
            continue

        # Flatten content (stringify if it’s not a string)
        if isinstance(content, list):
            flattened = " ".join(
                c.get("text", "") if isinstance(c, dict) else str(c)
                for c in content
            )
        else:
            flattened = str(content)

        if role == "system":
            processed.append({"role": "system", "content": flattened})

        elif role == "assistant":
            if not first_assistant_removed:
                first_assistant_removed = True
                continue
            else:
                processed.append({"role": "system", "content": flattened})

        elif role == "user":
            processed.append({"role": "user", "content": flattened})

    return processed

# --- AI Non-Streaming Function ---
def chat_completion(
    chat_history,
    api_key,
    model_name,
    max_tokens=150,
    top_p=1.0,
    api_version="2024-12-01-preview",
):
    """
    Sends a normal (non-streaming) chat completion request to HKBU GenAI API.
    """
    url = f"https://genai.hkbu.edu.hk/api/v0/rest/deployments/{model_name}/chat/completions?api-version={api_version}"

    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "Content-Type": "application/json",
    }

    payload = {
        "messages": chat_history,
        "max_tokens": max_tokens,
        "top_p": top_p,
        "stream": False,  # 👈 Ensure non-streaming mode
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        return {"error": f"[ERROR {response.status_code}] {response.text}"}

    return response.json()


# ------------------------------
# Non-Streaming Endpoint
# ------------------------------
@chatbot.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    chat_history = data.get("chat_history", [])
    api_key = data.get("api_key")
    model_name = data.get("model_name", "gpt-4")
    max_tokens = data.get("max_tokens", 150)
    top_p = data.get("top_p", 1.0)

    # ✅ Preprocess history here
    preprocessed_history = preprocess_chat_history(chat_history)
    # Call non-streaming API
    result = chat_completion(
        chat_history=preprocessed_history,
        api_key=api_key,
        model_name=model_name,
        max_tokens=max_tokens,
        top_p=top_p,
    )

    return jsonify(result)