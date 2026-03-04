# Voice-Driven Daily Activity Logging System

## System Overview

This system provides two ways to log daily activities via voice:

1. **Web App (Python/Flask)** - http://localhost:5001
2. **Telegram Bot** - Send voice messages to your Telegram bot

## Running Services

| Service | Port | URL |
|---------|------|-----|
| n8n | 5678 | http://localhost:5678 |
| Voice App | 5001 | http://localhost:5001 |

## Quick Start

```bash
cd /home/omart/n8n_logging
docker compose up -d
```

## Web App Usage

1. Open http://localhost:5001
2. Click the microphone button to start recording
3. Speak your activity (e.g., "I worked on the project for 2 hours")
4. Click again to stop recording
5. The app will:
   - Transcribe your voice
   - Extract structured data using Ollama (llama3.2)
   - Save to Obsidian vault

## Configuration

Environment variables in `.env`:
- `OLLAMA_API_KEY`: Your Ollama API key
- `OLLAMA_BASE_URL`: http://host.docker.internal:11434
- `OBSIDIAN_VAULT_PATH`: /data/obsidian

## Files

- `web-app/app.py` - Flask web application
- `web-app/templates/index.html` - Voice recorder UI
- `docker-compose.yml` - Docker configuration
- `obsidian-vault/` - Daily logs storage

## Daily Logs

Logs are saved to `obsidian-vault/daily-log-YYYY-MM-DD.md`
