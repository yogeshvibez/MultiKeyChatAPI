# chat_api.py
try:
    from flask import Flask, request, jsonify
    from openai import OpenAI
except ImportError:
    import subprocess
    import sys

    print("[*] Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "openai"])
    from flask import Flask, request, jsonify
    from openai import OpenAI

app = Flask(__name__)

# ⚙️ === CONFIGURATION === ⚙️
# 💡 Just change these to switch service

# Service: OpenAI / NVIDIA / AIMLAPI (Only 1 active at a time)
BASE_URL = "https://api.aimlapi.com/v1"  # Example: "https://api.openai.com/v1" or NVIDIA
MODEL_NAME = "openai/gpt-4.1-2025-04-14"  # Example: "gpt-3.5-turbo" or NVIDIA model

API_KEYS = [
    "c1e9b31cf2b64baabd9d434f9a60c833",
    "c1e9b31cf2b64baabd9d434f9a60c834"
]

# ==========================

def chat_with_fallback(messages):
    for key in API_KEYS:
        try:
            client = OpenAI(
                base_url=BASE_URL,
                api_key=key
            )

            print(f"[*] Trying key: {key[:8]}...")

            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=0.7,
                top_p=1.0,
                max_tokens=2048
            )

            return response.model_dump()

        except Exception as e:
            print(f"[!] Failed with key {key[:8]}...: {e}")
            continue

    return {"error": "All API keys failed."}


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data.get("messages")

    if not messages:
        return jsonify({"error": "Missing 'messages' in request body."}), 400

    result = chat_with_fallback(messages)
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
