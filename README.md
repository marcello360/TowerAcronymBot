# TowerAcronymBot 🎮

A Reddit bot that automatically detects and explains game acronyms in comments with progressively snarky responses. The bot monitors your subreddit and helps new players decode the esoteric alphabet soup that veteran players casually throw around.

## Features

✅ **Automatic Detection** - Scans subreddit comments for 125+ game acronyms (mods, cards, labs, workshop stats, etc.)  
✅ **Smart Matching** - Space-delimited detection to avoid false positives  
✅ **No Duplicates** - Tracks replied comments to prevent spam  
✅ **Progressive Snark** - Gets increasingly snarky based on how many acronyms it finds (1-2 = helpful, 11+ = roasting)  
✅ **GitHub Actions** - Runs automatically every 15 minutes from GitHub  
✅ **Easy Configuration** - Simple JSON file for adding/removing acronyms  
✅ **Comprehensive Logging** - Full activity logs in GitHub Actions

## How It Works

1. Bot scans the last 100 comments in your target subreddit
2. Checks each comment for known acronyms (e.g., AS, BH, GT, MVN, DWEW)
3. If acronyms are found, replies with explanations and attitude that scales with acronym count
4. Saves comment IDs to prevent duplicate replies
5. Repeats every 15 minutes via GitHub Actions

## Snark Levels

The bot adjusts its personality based on acronym density:
- **1-2 acronyms**: "Hi! I spotted an acronym..." (Friendly)
- **3-4 acronyms**: "Alright, let's decode this..." (Mildly snarky)
- **5-6 acronyms**: "Wow, someone's been drinking the acronym juice..." (Getting snarky)
- **7-8 acronyms**: "Oh good, a comment that reads like military code..." (Very snarky)
- **9-10 acronyms**: "*Deep breath* Okay. OKAY..." (Maximum snark)
- **11+ acronyms**: "ARE YOU KIDDING ME RIGHT NOW?..." (Nuclear snark)

## Setup Instructions

### 1. Create a Reddit Application

1. Go to https://www.reddit.com/prefs/apps
2. Click **"create another app..."** at the bottom
3. Fill in the form:
   - **name**: `TowerAcronymBot` (or your preferred name)
   - **App type**: Select **"script"**
   - **description**: Optional description
   - **about url**: Leave blank or add your GitHub repo URL
   - **redirect uri**: `http://localhost:8080` (required but not used)
4. Click **"create app"**
5. Note down:
   - **client_id**: The string under "personal use script"
   - **client_secret**: The string next to "secret"

### 2. Create a Reddit Account for the Bot

1. Create a new Reddit account specifically for your bot
2. Verify the email address
3. Note down the username and password

### 3. Fork/Clone This Repository

```bash
git clone https://github.com/marcello360/TowerAcronymBot.git
cd TowerAcronymBot
```

### 4. Configure GitHub Secrets

Your Reddit credentials need to be stored as GitHub Secrets (encrypted):

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"** and add each of the following:

| Secret Name | Value |
|-------------|-------|
| `REDDIT_CLIENT_ID` | Your app's client ID from step 1 |
| `REDDIT_CLIENT_SECRET` | Your app's client secret from step 1 |
| `REDDIT_USERNAME` | Your bot account username |
| `REDDIT_PASSWORD` | Your bot account password |
| `SUBREDDIT_NAME` | Target subreddit name (without `r/`) |

**Example**: If monitoring `r/aviation`, set `SUBREDDIT_NAME` to `aviation`

### 5. Enable GitHub Actions

1. Go to the **Actions** tab in your repository
2. Click **"I understand my workflows, go ahead and enable them"**
3. The bot will now run automatically every 15 minutes

### 6. Manual Trigger (Optional)

You can manually trigger the bot:

1. Go to **Actions** tab
2. Select **"TowerAcronymBot Scheduler"**
3. Click **"Run workflow"** → **"Run workflow"**

## Local Testing

To test the bot locally before deploying:

### 1. Install Python 3.9+

```bash
python --version  # Should be 3.9 or higher
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create `.env` File

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```env
REDDIT_CLIENT_ID=your_actual_client_id
REDDIT_CLIENT_SECRET=your_actual_client_secret
REDDIT_USERNAME=your_bot_username
REDDIT_PASSWORD=your_bot_password
SUBREDDIT_NAME=test  # Use a test subreddit first!
```

### 4. Run the Bot

```bash
python bot.py
```

**⚠️ Important**: Test on a low-traffic subreddit first (like `r/test` or your own private subreddit)!

## Configuration

### Adding/Modifying Acronyms

Edit `acronyms.json`:

```json
{
  "ATC": "Air Traffic Control",
  "VFR": "Visual Flight Rules",
  "YOUR_ACRONYM": "Your explanation here"
}
```

**After editing:**
- Commit and push changes to GitHub
- The bot will automatically use the updated list on next run

### Adjusting Run Frequency

Edit `.github/workflows/bot-schedule.yml`:

```yaml
schedule:
  - cron: '*/15 * * * *'  # Every 15 minutes
  # Change to '*/30 * * * *' for every 30 minutes
  # Change to '0 * * * *' for every hour
```

**Cron Format**: `minute hour day month weekday`

**⚠️ GitHub Actions Limitation**: Minimum interval is ~5 minutes, but may run less frequently during high GitHub traffic.

### Adjusting Scan Depth

Edit the `limit` parameter in `bot.py` (line ~165):

```python
def scan_subreddit(self, limit: int = 100):  # Change 100 to scan more/fewer comments
```

## File Structure

```
TowerAcronymBot/
├── .github/
│   └── workflows/
│       └── bot-schedule.yml       # GitHub Actions configuration
├── bot.py                          # Main bot logic
├── acronyms.json                   # Acronym definitions (editable)
├── replied_comments.json           # State file (auto-generated)
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## How Replies Look

### Example 1: Friendly (2 acronyms)
> Hi! I detected a couple acronyms in your comment:
> 
> - **BH** - Black Hole ultimate weapon
> - **GT** - Golden Tower ultimate weapon
> 
> ---
> *I'm a bot that explains acronyms*

### Example 2: Snarky (6 acronyms)
> Wow, someone's been drinking the acronym juice. Here's the translation:
> 
> - **AS** - Amplifying Strike cannon mod
> - **BHD** - Black Hole Digestor generator mod
> - **MVN** - Multiverse Nexus core mod
> - **DWEW** - Death Wave Effective Wave
> - **GC** - Glass Cannon
> - **PWR** - Perk Wave Requirement
> 
> ---
> *I'm a bot | Because full words are apparently too mainstream*

### Example 3: Nuclear Snark (11+ acronyms)
> ARE YOU KIDDING ME RIGHT NOW? Did you just have a stroke on your keyboard or are you genuinely trying to communicate? Fine. FINE. Here's your dissertation translated:
> 
> - **AS** - Amplifying Strike cannon mod
> - **ASPD** - Attack Speed workshop stat
> - **BH** - Black Hole ultimate weapon
> - **CF** - Chrono Field ultimate weapon
> - **DW** - Death Wave ultimate weapon
> - **GT** - Golden Tower ultimate weapon
> - **MVN** - Multiverse Nexus core mod
> - **eHP** - Effective Health Points
> - **GC** - Glass Cannon
> - **ROI** - Return on Investment
> - **WAWSIS** - Wave Accelerator + Wave Skip + Intro Sprint
> 
> ---
> *I'm a bot | This is my villain origin story | You did this*

## Monitoring

### View Bot Activity

1. Go to **Actions** tab in your repository
2. Click on any workflow run to see logs
3. Expand **"Run TowerAcronymBot"** step to see detailed output

### Check State File

The `replied_comments.json` file tracks:
- All comment IDs that have been replied to
- Last run timestamp
- Total number of replies

## Troubleshooting

### Bot Not Running

- ✅ Check that GitHub Actions are enabled
- ✅ Verify all 5 secrets are set correctly
- ✅ Check Actions tab for error logs
- ✅ Ensure repository is not private (or you have Actions minutes)

### Bot Not Replying

- ✅ Check that acronyms exist in `acronyms.json`
- ✅ Verify the bot account has enough karma (some subreddits have restrictions)
- ✅ Check if comments are too old (bot scans recent comments only)
- ✅ Review GitHub Actions logs for errors

### Rate Limit Errors

- ✅ Reduce scan frequency (e.g., every 30 minutes instead of 15)
- ✅ Reduce `limit` parameter in `bot.py`
- ✅ PRAW automatically handles rate limits, but errors may occur if too aggressive

### "Invalid Credentials" Error

- ✅ Double-check all GitHub Secrets are set correctly
- ✅ Ensure no extra spaces in secret values
- ✅ Verify Reddit app is set to "script" type
- ✅ Confirm bot account password is correct

### Bot Replies to Own Comments

This shouldn't happen - the code explicitly checks for this. If it does:
- Check that `REDDIT_USERNAME` matches the bot account exactly

## Best Practices

1. **Start Small**: Test on a private or low-traffic subreddit first
2. **Monitor Frequently**: Check Actions logs after initial deployment
3. **Respect Subreddit Rules**: Ensure the subreddit allows bots
4. **Be Helpful**: Only add acronyms relevant to your game/community
5. **Rate Limits**: Don't set the frequency too high (15 minutes is recommended)
6. **Community Feedback**: Monitor comment replies and adjust snark levels if needed
7. **Acronym Quality**: Keep definitions accurate and up-to-date with game updates

## Reddit Bot Guidelines

- ✅ Always identify as a bot in your username (e.g., ending with "Bot")
- ✅ Add bot footer with source link
- ✅ Respect subreddit rules about bots
- ✅ Don't spam - track replied comments
- ✅ Respond to "stop" requests from users
- ✅ Be transparent about what your bot does

## Contributing

Feel free to:
- Add more acronyms to `acronyms.json`
- Improve the bot logic in `bot.py`
- Submit issues or pull requests

## License

This project is provided as-is for educational purposes. Use responsibly and in accordance with Reddit's [API Terms of Use](https://www.reddit.com/wiki/api-terms).

## Disclaimer

This bot is not affiliated with Reddit or any game developer. Acronym explanations are provided for informational purposes only. The snark is purely for entertainment.

---

**Happy gaming! 🎮**
