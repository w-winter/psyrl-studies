# Psychedelic Studies Tracker

Automated tracker for new IRL psychedelic studies posted on the Atlas of Psychedelic Research.

## Setup

1. Clone this repository
2. If you want an initial set of notifications covering all extant studies in the Atlas, run `git rm studies.db` and commit the change.
3. Set up the Discord webhook:
   - Create the channel within your Discord server where you want to receive the notifications
   - Go to Server Settings > Integrations > Create Webhook
   - Select the name of that specific channel (the webhook must post to this specific channel)
   - Copy the webhook URL - it should look like `https://discord.com/api/webhooks/...`
4. Add the webhook URL as a repository secret:
   - Go to your GitHub repository Settings
   - Navigate to Secrets and variables > Actions
   - Click "New repository secret"
   - Name: `DISCORD_WEBHOOK_URL`
   - Value: Paste the webhook URL you copied

## Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variable
export DISCORD_WEBHOOK_URL='your_webhook_url_here'  # Unix/Mac

# Run the script
python src/main.py
```

## GitHub Actions

The script runs automatically every day at 4 minutes and 20 seconds after midnight UTC via GitHub Actions.  You can also trigger it manually from the Actions tab in your repository.

## Database

The SQLite database (`studies.db`) is committed to the repository and updated automatically when new studies are found.
