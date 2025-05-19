# Auto-install dependencies
try:
    from flask import Flask, request, jsonify
    import requests
except ImportError:
    import subprocess
    import sys

    print("[*] Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "requests"])

    # Retry import after installation
    from flask import Flask, request, jsonify
    import requests

app = Flask(__name__)

# Common base URL
BASE_URL = "https://models.github.ai/inference/chat/completions"

# Only API keys now
API_KEYS = [
    "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",  # Primary
    "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"   # Fallback
]

def call_api(messages):
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-4.1",
        "messages": messages,
        "temperature": 1,
        "top_p": 1
    }

    for key in API_KEYS:
        try:
            headers["Authorization"] = f"Bearer {key}"
            response = requests.post(
                BASE_URL,
                headers=headers,
                json=payload,
                timeout=15
            )

            print(f"[*] Trying with key {key[:8]}... - Status: {response.status_code}")

            if response.status_code == 200:
                return response.json()

            print("[!] Failed:", response.status_code, response.text)

        except Exception as e:
            print("[x] Error:", e)

    return {"error": "All API calls failed."}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data.get("messages")

    if not messages:
        return jsonify({"error": "Missing 'messages'"}), 400

    result = call_api(messages)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
