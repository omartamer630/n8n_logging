from flask import Flask, render_template, request, jsonify
import os
import requests
import json
from datetime import datetime

app = Flask(__name__)

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "ee4f834fdc17490b8841f20e017663de.1aW39FgtIJVGNGi7GeDQdxoD")
OLLAMA_URL = "https://ollama.com/api/chat"
OBSIDIAN_PATH = "/data/obsidian"

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
            {"role": "system", "content": "Extract from user input: start_time (HH:MM), end_time (HH:MM), activity, mood. Return ONLY valid JSON like: {\"start_time\":\"09:00\",\"end_time\":\"10:30\",\"activity\":\"Working\",\"mood\":\"happy\"}"},
            {"role": "user", "content": text}
        ],
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
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
                    return json.loads(content[start:end])
            except:
                pass
    except Exception as e:
        print(f"Ollama error: {e}")

    # Fallback
    now = datetime.now().strftime("%H:%M")
    return {"start_time": now, "end_time": now, "activity": text[:50], "mood": "neutral"}

def save_to_obsidian(data):
    """Save to daily log"""
    today = datetime.now().strftime("%Y-%m-%d")
    os.makedirs(f"{OBSIDIAN_PATH}/DailyLogs", exist_ok=True)
    filepath = f"{OBSIDIAN_PATH}/DailyLogs/{today}.md"

    content = f"\n| {data.get('start_time','')} | {data.get('end_time','')} | {data.get('duration','')} | {data.get('activity','')} | {data.get('mood','')} |\n"

    with open(filepath, 'a', encoding='utf-8') as f:
        # Add header if new file
        if os.path.getsize(filepath) == 0:
            f.write("| Start | End | Duration | Activity | Mood |\n")
            f.write("|-------|-----|----------|----------|------|\n")
        f.write(content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
