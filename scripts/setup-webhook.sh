#!/bin/bash
# Setup Telegram Bot Webhook

# Load environment variables
source .env

# Set the webhook URL
WEBHOOK_URL="${WEBHOOK_URL}/telegram-voice"

echo "Setting up Telegram bot webhook..."
echo "Webhook URL: $WEBHOOK_URL"

# Set the webhook
curl -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" \
  -H "Content-Type: application/json" \
  -d "{\"url\": \"$WEBHOOK_URL\"}"

echo ""
echo "Webhook setup complete!"
