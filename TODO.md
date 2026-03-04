## TODO – Voice‑Based Daily Logging System

1. **Verify workflow logic** – Confirm that each node (Webhook → Get File → Download → Whisper → LLM → Write) works end‑to‑end.
2. **Add retry nodes** – Wrap Whisper and LLM nodes with a *Retry* node (max 3 attempts, exponential back‑off).
3. **Validate time parsing** – Ensure the LLM prompt reliably returns `HH:MM` or `null`. If `null`, trigger a *Telegram Send Message* node to ask the user for missing times.
4. **Prevent duplicates** – Before writing, check if the entry already exists in the day's Markdown file. If so, skip or update.
5. **Error logging** – Configure *Write Binary File* node to write any failures to `logs/error.log`.
6. **Health‑check** – Verify the Docker‑Compose healthcheck pings n8n’s `/status` endpoint.
7. **Security audit** – Review secrets handling, ensure `.env` is in `.gitignore`, and confirm no sensitive data is logged.
8. **Documentation** – Update `README.md`, `ARCHITECTURE.md`, and add a `CONTRIBUTING.md`.
9. **Testing** – Write unit‑style tests for the n8n workflow (mock Telegram & Ollama responses) if possible.
10. **Deployment checklist** – Outline steps for production: Docker‑Compose up‑to‑date, TLS for webhook, continuous backup of Obsidian vault.
11. **Final report** – Draft `FINAL_REPORT.md` summarizing architecture, decisions, scaling, and security posture.
12. **Code review** – Ask a teammate to review the workflow and docs.

**Status**: In progress (task #1)
