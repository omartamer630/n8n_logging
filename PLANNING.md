# PLANNING

## 1. System Architecture Diagram (ASCII)
```
    +-------------------+         +---------------------+
    |   Telegram Bot    |         |   Ollama   |
    | (HTTP/Webhook)    |         | (Transcription)   |
    +-------------------+  <--->  +---------------------+
            |                                   |
            |                                   |
            v                                   v
    +-------------------+         +---------------------+
    |    n8n (Docker)   |         |   Obsidian Vault    |
    | (Workflow Engine) |         | (File System)      |
    +-------------------+  <--->  +---------------------+
```

Key responsibilities:
- **Telegram Bot**: Receives voice messages, sends HTTP webhook to n8n.
- **n8n**: Orchestrates the following:
  1. Saves incoming audio to a temp directory.
  2. Calls Ollama to transcribe.
  3. Formats the transcript into a Markdown file timestamped for the day.
  4. Writes the file into the mounted Obsidian vault.
- **Ollama**: Speech‑to‑text service.
- **Obsidian Vault**: Persistent filing surface for notes.

All communication is over HTTPS. Secrets are injected via Docker‑Compose environment variables.

---

## 2. Component Breakdown

| Component | Purpose | Key Traits |
|-----------|---------|-------------|
| **Telegram Bot** | Accepts voice messages from users | Runs on Telegram's webhook server, transfers audio file via HTTPS |
| **n8n** | Core workflow engine | Node‑based, self‑hosted, Docker image `n8nio/n8n` |
| **Ollama Node** | Speech‑to‑text | HTTP API call, requires `OPENAI_API_KEY` |
| **Obsidian Vault** | Storage backend | Simple file system folder, mounts as Docker volume |
| **Docker Compose** | Orchestration | Declares services, volumes, health‑check |

### n8n Workflow specifics
- Trigger: `Webhook` node (incoming audio)
- `HTTP Request` node (upload to Whisper)
- `Set` node (format timestamp, path)
- `Write Binary File` node (write Markdown to attached volume)
- **Retry** node or timeout handling for API failures.

---

## 3. Security Model

- **Secret Injection**: Secrets entered in `.env` file are mounted as environment variables; `.env` is ignored by `.gitignore`.
- **TLS**: All external HTTP traffic is encrypted. Telegram expects HTTPS webhooks; we may provision a TLS cert via `nginx` reverse proxy or expose on public domain.
- **Least Privilege**: n8n container runs as non‑root (`n8n` user). Volumes are mounted read/write only within required folders.
- **Network Isolation**: Docker network isolates n8n from other services. Telegram webhooks reach n8n via host port mapping, optionally behind reverse proxy.

## 4. Data Flow
1. User sends voice message to Telegram Bot.
2. Telegram forwards audio file to n8n webhook via HTTPS.
3. n8n receives audio, stores binary in a temp path.
4. n8n calls Ollama API with audio, receives JSON transcript.
5. n8n formats transcript + metadata into Markdown.
6. n8n writes file into Obsidian vault (e.g., `notes/<YYYY‑MM‑DD>.md`).
7. User can access note via Obsidian or version control.

All intermediate data (audio, transcript) is transient; no persistence beyond n8n's runtime unless stored in the vault.

---

## 5. Failure Handling Strategy
- **Webhook retry**: Telegram automatically retries if HTTP 5xx; n8n can detect failures.
- **Whisper API errors**: n8n uses a `Retry` node (max 3 attempts, exponential back‑off). If still failing, log error and optionally send alert to Telegram.
- **File write errors**: n8n will retry write; if volume unavailable, pipeline fails and an error node sends a notification.
- **Logging**: All steps log to n8n's internal logger; optionally persist to a file via `Execute & Cache` node.
- **Health‑check**: Docker Compose health‑check pings n8n's health endpoint; if unhealthy, service restarts automatically.

## 6. Secret Management Approach
- `.env` file (example ` .env.example` ) contains placeholders for:
  - `TELEGRAM_BOT_TOKEN`
  - `OPENAI_API_KEY`
- Users will copy `.env.example` to `.env`, then export variables or provide via Docker Compose override.
- `.gitignore` excludes `.env` so secrets never enter repo.
- For additional safety, sensitive values can be provided via Docker secrets or a vault (not implemented in this prototype).

## 7. Trade‑offs Considered
| Consideration | Option A | Option B | Decision |
|----------------|---------|---------|---------|
| Transcription | Ollama (cloud) | Local Whisper Docker | **Whisper** chosen for accuracy and simplicity; local option adds CPU/memory needs |
| Bot Platform | Telegram | Discord | Telegram selected due to ease of voice message receipt |
| Workflow engine | n8n | Custom Node.js | n8n reduces development effort but less fine‑grained control |
| Storage | File system (Obsidian) | Database | File system chosen to integrate directly with Obsidian; DB would add complexity |
| Security | Docker secrets | Env vars | Env vars used for simplicity; adding secrets is straightforward if needed |

---

## 8. Next Steps
1. Bootstrap repo structure (files, directories, placeholder documentation).
2. Draft Docker‑Compose file with n8n service, volume mounts, health‑check.
3. Design and create n8n workflow JSON (voice‑logger.json) with above nodes.
4. Add `.env.example`, README, architecture docs.
5. Commit each logical phase.
6. Ask for any required credentials.
7. Proceed to implementation upon approval.

Please review this plan and let me know if it meets your expectations or if you would like any adjustments before we create the repository structure.
