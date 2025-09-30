# TowerAcronymBot 🎮

A Reddit bot that automatically detects and explains game acronyms in comments with progressively snarky responses. The bot helps new players decode the esoteric alphabet soup that veteran players casually throw around.

## Features

✅ **Automatic Detection** - Scans subreddit comments for 125+ game acronyms (mods, cards, labs, workshop stats, etc.)  
✅ **Smart Matching** - Space-delimited detection to avoid false positives  
✅ **No Duplicates** - Tracks replied comments to prevent spam  
✅ **Progressive Snark** - Gets increasingly snarky based on how many acronyms it finds (1-2 = helpful, 11+ = roasting)  
✅ **GitHub Actions** - Runs automatically every 15 minutes  
✅ **Easy Configuration** - Simple JSON file for adding/removing acronyms

## How It Works

The bot scans recent comments in the subreddit, detects acronyms from its database, and replies with explanations. The tone scales with the number of acronyms found - from friendly and helpful to hilariously exasperated.

## Snark Levels

The bot adjusts its personality based on acronym density:
- **1-2 acronyms**: Friendly and helpful
- **3-4 acronyms**: Mildly snarky
- **5-6 acronyms**: Getting snarky
- **7-8 acronyms**: Very snarky  
- **9-10 acronyms**: Maximum snark
- **11+ acronyms**: Nuclear snark

## Example Replies

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

---

**Happy gaming! 🎮**
