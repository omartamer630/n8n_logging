# Implementation Steps

## 1. Repository Structure
Create the following directories and placeholder files:
```
├── README.md
├── PLANNING.md
├── ARCHITECTURE.md
├── IMPLEMENTATION_STEPS.md
├── docker-compose.yml
├── .env.example
├── workflows/
│   └── voice-logger.json
├── obsidian-vault/   (empty folder)
└── scripts/           (empty folder)
```

## 2. Docker‑Compose Setup
Define a single `n8n` service with:
- `n8nio/n8n` image
- Port mapping `5678:5678`
- Environment variables for secrets (`TELEGRAM_BOT_TOKEN`, `OPENAI_API_KEY`)
- Volume mounts:
  - `./obsidian-vault:/home/n8n/obsidian-vault` for notes
  - `./workflows:/home/n8n/workflows:ro` for workflow JSON
  - `n8n_data:/data` persistent data
- Health‑check that curls `http://localhost:5678/status`

## 3. n8n Workflow (`voice-logger.json`)
Build a JSON representation of the workflow containing:
- **Webhook Trigger**: Listens on `/telegram-voice`
- **HTTP Request** (OpenAI Whisper): POST audio file, parse response
- **Set** node: create `YYYY-MM-DD.md` filename, compute timestamp
- **Write Binary File** node: write the Markdown content to `obsidian-vault` directory
- **Error Handling**: Add Retry nodes on Whisper and Write steps

## 4. Secrets Management
Copy `.env.example` to `.env`, replace placeholders with actual values:
```
TELEGRAM_BOT_TOKEN=your-telegram-token
OPENAI_API_KEY=your-openai-key
```
Ensure `.env` is listed in `.gitignore`.

## 5. Documentation
Populate:
- `README.md` with project overview & instructions
- `ARCHITECTURE.md` with diagram (see PLANNING)
- `PLANNING.md` (already provided)
- `FINAL_REPORT.md` to be generated after implementation is complete.

## 6. Deployment
```
docker compose up -d
```
Verify that n8n is reachable at `http://localhost:5678` and that the Webhook endpoint `/telegram-voice` is exposed.

---

**Next step:** Create the Docker‑Compose file, workflow JSON, and volume placeholders. Will seek approval before proceeding.
