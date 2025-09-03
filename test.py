import requests
import json

url = "https://genai.hkbu.edu.hk/api/v0/rest/deployments/gpt-4.1/chat/completions?api-version=2024-12-01-preview"

headers = {
    "accept": "application/json",
    "api-key": "f78e26ce-5d62-455a-a4f6-055df1fc1a27",
    "Content-Type": "application/json"
}

payload = {
    "messages": [
        {
            "role": "system",
            "content": "You are a friendly helper! Talk to the user like they are 3 years old. Use very simple words, be super excited and happy, and explain everything in a fun way that a little kid would understand!"
        },
        {
            "role": "user",
            "content": "Hello! Can you help me write a Python function to calculate the factorial of a number?"
        }
    ],
    "max_tokens": 150,
    "top_p": 1,
    "stream": True
}

# Send request with streaming enabled
with requests.post(url, headers=headers, json=payload, stream=True) as response:
    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
    else:
        for line in response.iter_lines():
            if line:
                # The API uses "data: ..." format for streaming
                decoded_line = line.decode("utf-8").strip()
                if decoded_line.startswith("data: "):
                    data = decoded_line[len("data: "):]
                    if data == "[DONE]":
                        print("\n--- Stream finished ---")
                        break
                    try:
                        event = json.loads(data)
                        delta = event["choices"][0]["delta"].get("content", "")
                        if delta:
                            print(delta)
                    except Exception as e:
                        print("\n[Error parsing stream chunk]", decoded_line, e)