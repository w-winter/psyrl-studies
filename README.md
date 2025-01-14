# IRL Psychedelic Studies Tracker

Automated tracker for new studies posted on the Atlas of Psychedelic Research.

## Setup

1. Create a new GitHub repository and clone it
2. Copy these files into the repository
3. Set up the Discord webhook:
   - Create a channel named exactly `#psyrl-studies` in your Discord server
   - Go to Server Settings > Integrations > Create Webhook
   - Name it "PsyRL Studies Bot"
   - IMPORTANT: Set the channel to `#psyrl-studies` - the webhook must post to this specific channel
   - Copy the webhook URL - it should look like `https://discord.com/api/webhooks/...`
4. Add the webhook URL as a repository secret:
   - Go to your GitHub repository Settings
   - Navigate to Secrets and variables > Actions
   - Click "New repository secret"
   - Name: `DISCORD_WEBHOOK_URL`
   - Value: Paste the webhook URL you copied
   - Click "Add secret"

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

The script runs automatically every day at midnight UTC via GitHub Actions. You can also trigger it manually from the Actions tab in your repository.

## Database

The SQLite database (`studies.db`) is committed to the repository and updated automatically when new studies are found.

## Verification

Before leaving the setup running, verify that:
1. A channel named exactly `#psyrl-studies` exists in your Discord server
2. The webhook is configured to post to `#psyrl-studies` (check Server Settings > Integrations)
3. The test run (triggered manually from GitHub Actions) successfully posts to `#psyrl-studies`

If messages appear in the wrong channel, delete the webhook and recreate it with the correct channel selected.