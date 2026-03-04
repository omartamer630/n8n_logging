# Architecture

The architecture is documented in detail in `PLANNING.md`. For reference, the main components are:

- **Telegram Bot**: Receives voice messages via webhook.
- **n8n**: Executes the workflow: store audio, transcribe via Whisper, write Markdown to Obsidian vault.
- **Obsidian Vault**: Folder mounted in the n8n container to persist notes.

This repo contains a Docker‑Compose stack running n8n with a health‑check and volume mounts.
