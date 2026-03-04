# Final Report

The following report summarizes the design, decisions, and operational aspects of the Voice‑Driven Daily Activity Logging system.

## Architecture Overview
```
+-------------------+      HTTPS      +-----------------------+
|  Telegram Bot   |<-------------->|  n8n Workflow Engine   |
+-------------------+                  +-----------------------+
          |                                        |
          |  Webhook                                |  HTTP
          |                                        |
          V                                        V
+------------------------------+   POST   +--------------------------+
|  Ollama Cloud – Whisper      |<--------|  Transcription Result   |
+------------------------------+          +--------------------------+
          |                                        |
          |  HTTP  ➜ LLM (Ollama)   +---------------------+
          V                        |  Structured JSON     |
+--------------------------+      +---------------------+
|  Obsidian Vault (File)   |<-----|  Daily Log Markdown |
+--------------------------+      +---------------------+
```

### Key Components
| Component | Role |
|-----------|------|
| **Telegram Bot** | Receives voice notes via webhook.
| **n8n** | Orchestrates: download audio, call Whisper, LLM extraction, write journal.
| **Ollama Whisper** | Speech‑to‑text (Arabic).
| **Ollama LLM** | Extracts structured JSON from transcript.
| **Obsidian Vault** | Persistent storage of daily logs.
| **Docker‑Compose** | Container orchestration, secrets, health‑checks.

## Functional Flow
1. User sends a voice note on Telegram.
2. Telegram forwards the message to n8n via the `/telegram-voice` webhook.
3. n8n obtains the file link, downloads the audio.
4. Audio is sent to the Ollama Whisper endpoint.
5. Whisper returns a transcript (Arabic).
6. Transcript is fed to an Ollama LLM (model `gpt4` in this example) with a prompt to output JSON containing `start_time`, `end_time`, `activity`, `mood`.
7. The workflow checks if `start_time` or `end_time` is `null`. If missing, a *Telegram Send Message* node would normally ask the user; for this simplified prototype the workflow logs the issue and aborts.
8. If times are present, the workflow calculates `duration`, constructs a Markdown table row, and appends it to `./obsidian-vault/DailyLogs/YYYY-MM-DD.md`.
9. Any API call that fails triggers an automatic *Retry* node (3 attempts, exponential back‑off). Errors are logged to `logs/error.log`.

## Security and Secrets
| Secret | Storage | Access |
|--------|---------|--------|
| `TELEGRAM_BOT_TOKEN` | `.env` | injected into n8n env |
| `OLLAMA_API_KEY` | `.env` | injected into n8n env |
| `OLLAMA_ENDPOINT` | `.env` (optional) | default is `https://api.ollama.ai/api/invoke/whisper` |
The `.env` file is excluded from Git (`.gitignore`) and mounted as an env file by Docker‑Compose.

## Reliability & Failure Handling
| Event | Handling |
|-------|----------|
| Telegram webhook timeout | Telegram retries; n8n receives multiple attempts but only processes once due to dedup logic (not implemented in this prototype). |
| Whisper API failure | *Retry* node (max 3 attempts). If still failing, error logs are written and the workflow ends with an error node. |
| LLM extraction failure | Same retry logic; if JSON validation fails, log and abort. |
| Missing time data | Node would prompt the user; current implementation logs error and skips write. |
| Disk write failure | Write node retries; logs error to `logs/error.log`. |

## Operational Notes
- **Start it**: `docker compose up -d`
- **Access UI**: `http://localhost:5678`
- **Workflow Import**: Import `workflows/voice-logger.json` via the UI.
- **Telegram Webhook**: Point bot webhook to `https://<public-domain>/integration/telegram-voice`.
- **Logs**: View error logs at `logs/error.log`. Docker logs are available via `docker compose logs n8n`.
- **Scaling**: Since n8n is stateless (data stored in volume), you can run multiple n8n containers behind a load balancer and mount the same volumes; Ollama must be accessible via a stable endpoint.

## Trade‑offs
- **Accuracy vs. Cost**: Using Ollama Whisper locally would reduce API cost but requires CPU/GPU resources; we opted for cloud service for simplicity.
- **Language Support**: Whisper handles Arabic well; LLM prompt parsing may need adjustments for dialects.
- **Duplicate Prevention**: Simple checksum mechanism not yet implemented; can be added by hashing entries.
- **Security**: Secrets are only in Docker env; consider Docker secrets for production.

---

**Prepared by Claude Code**
`EOF`
