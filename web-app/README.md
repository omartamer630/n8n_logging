# Python Web Voice Logger

This is a web-based voice recording application that:
1. Records voice in browser
2. Sends to Ollama for transcription
3. Uses Ollama to extract structured JSON
4. Saves to Obsidian vault

## Quick Start

```bash
cd /home/omart/n8n_logging
docker compose up -d
```

Then open: http://localhost:5679

## Environment Variables

All configuration is in `.env` file.
