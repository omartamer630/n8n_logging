from flask import Flask, render_template, request, jsonify
import os
import requests
import json
from datetime import datetime

app = Flask(__name__)

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "ee4f834fdc17490b8841f20e017663de.1aW39FgtIJVGNGi7GeDQdxoD")
OLLAMA_CHAT_URL = "https://api.ollama.ai/api/chat"
OBSIDIAN_PATH = os.getenv("OBSIDIAN_VAULT_PATH", "/data/obsidian")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/submit-text', methods=['POST'])
def submit_text():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        # Extract structured data with Ollama
        structured = extract_data(text)

        # Save to Obsidian
        save_to_obsidian(structured)

        return jsonify({
            'success': True,
            'data': structured
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def extract_data(text):
    """Use Ollama to extract structured JSON"""
    payload = {
        "model": "qwen3.5:397b",
        "messages": [
            {"role": "system", "content": "Extract start_time (HH:MM 24h), end_time (HH:MM 24h), activity, mood from the transcript. Return ONLY valid JSON like: {\"start_time\":\"09:00\",\"end_time\":\"10:30\",\"activity\":\"Working\",\"mood\":\"happy\"}"},
            {"role": "user", "content": text}
        ],
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_CHAT_URL,
            json=payload,
            headers={
                "Authorization": f"Bearer {OLLAMA_API_KEY}",
                "Content-Type": "application/json"
            },
            timeout=30
        )

        if response.status_code == 200:
            content = response.json().get('message', {}).get('content', '')
            # Parse JSON from response
            try:
                if '{' in content:
                    start = content.find('{')
                    end = content.rfind('}') + 1
                    parsed = json.loads(content[start:end])

                    # Calculate duration
                    try:
                        sh, sm = parsed.get('start_time', '').split(':')
                        eh, em = parsed.get('end_time', '').split(':')
                        duration = (int(eh) * 60 + int(em)) - (int(sh) * 60 + int(sm))
                        if duration < 0:
                            duration = ''
                        parsed['duration'] = duration
                    except:
                        parsed['duration'] = ''

                    return parsed
            except:
                pass
    except Exception as e:
        print(f"Ollama error: {e}")

    # Fallback
    now = datetime.now().strftime("%H:%M")
    return {"start_time": now, "end_time": now, "duration": "", "activity": text[:50], "mood": "neutral"}

def save_to_obsidian(data):
    """Save to daily log"""
    today = datetime.now().strftime("%Y-%m-%d")
    os.makedirs(f"{OBSIDIAN_PATH}/DailyLogs", exist_ok=True)
    filepath = f"{OBSIDIAN_PATH}/DailyLogs/{today}.md"

    content = f"| {data.get('start_time','')} | {data.get('end_time','')} | {data.get('duration','')} | {data.get('activity','')} | {data.get('mood','')} |\n"

    # Check if file is new and add header
    file_exists = os.path.exists(filepath)
    file_empty = not file_exists or os.path.getsize(filepath) == 0

    with open(filepath, 'a', encoding='utf-8') as f:
        if file_empty:
            f.write("| Start | End | Duration | Activity | Mood |\n")
            f.write("|-------|-----|----------|----------|------|\n")
        f.write(content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
