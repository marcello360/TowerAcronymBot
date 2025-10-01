"""
TowerAcronymBot - Reddit bot that detects and explains acronyms in comments.
"""

import os
import json
import re
import logging
from datetime import datetime
from typing import Dict, List, Set
import praw
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# File paths
ACRONYMS_FILE = 'acronyms.json'
STATE_FILE = 'replied_comments.json'


class TowerAcronymBot:
    """Main bot class for scanning and responding to acronyms."""
    
    def __init__(self):
        """Initialize the bot with Reddit credentials and load configuration."""
        load_dotenv()
        
        # Load Reddit credentials
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            username=os.getenv('REDDIT_USERNAME'),
            password=os.getenv('REDDIT_PASSWORD'),
            user_agent=f'TowerAcronymBot v1.0 by u/{os.getenv("REDDIT_USERNAME")}'
        )
        
        self.subreddit_name = os.getenv('SUBREDDIT_NAME')
        self.subreddit = self.reddit.subreddit(self.subreddit_name)
        
        # Load acronyms and state
        self.acronyms = self.load_acronyms()
        self.replied_comments = self.load_replied_comments()
        
        logger.info(f"Bot initialized. Monitoring r/{self.subreddit_name}")
        logger.info(f"Loaded {len(self.acronyms)} acronyms")
    
    def load_acronyms(self) -> Dict[str, str]:
        """Load acronym definitions from JSON file."""
        try:
            with open(ACRONYMS_FILE, 'r', encoding='utf-8') as f:
                acronyms = json.load(f)
                logger.info(f"Loaded {len(acronyms)} acronyms from {ACRONYMS_FILE}")
                return acronyms
        except FileNotFoundError:
            logger.error(f"{ACRONYMS_FILE} not found!")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing {ACRONYMS_FILE}: {e}")
            return {}
    
    def load_replied_comments(self) -> Set[str]:
        """Load set of comment IDs that have already been replied to."""
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                replied_ids = set(data.get('replied_ids', []))
                logger.info(f"Loaded {len(replied_ids)} replied comment IDs")
                return replied_ids
        except FileNotFoundError:
            logger.info(f"{STATE_FILE} not found. Starting fresh.")
            return set()
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing {STATE_FILE}: {e}")
            return set()
    
    def save_replied_comments(self):
        """Save the current state of replied comments to JSON file."""
        try:
            data = {
                'replied_ids': list(self.replied_comments),
                'last_run': datetime.utcnow().isoformat(),
                'total_replies': len(self.replied_comments)
            }
            with open(STATE_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Saved state: {len(self.replied_comments)} total replies")
        except Exception as e:
            logger.error(f"Error saving state file: {e}")
    
    def find_acronyms(self, text: str) -> List[str]:
        """
        Find all known acronyms in the given text.
        Only matches acronyms that are surrounded by spaces (or start/end of string).
        
        Args:
            text: The comment text to search
            
        Returns:
            List of acronyms found (in order of appearance, no duplicates)
        """
        found_acronyms = []
        seen = set()
        
        # Convert text to uppercase for matching
        text_upper = text.upper()
        
        for acronym in self.acronyms.keys():
            # Create regex pattern requiring spaces (or string boundaries) around the acronym
            # (?:^|\s) matches start of string or whitespace
            # (?:\s|[.,!?;:)]|$) matches whitespace, common punctuation, or end of string
            # Don't match if followed by + or % (for things like UW+, DEF%)
            pattern = r'(?:^|\s)' + re.escape(acronym.upper()) + r'(?:\s|[.,!?;:)]|$)'
            
            if re.search(pattern, text_upper):
                # Preserve original case from acronyms.json
                if acronym not in seen:
                    found_acronyms.append(acronym)
                    seen.add(acronym)
        
        return found_acronyms
    
    def format_response(self, acronyms: List[str]) -> str:
        """
        Format the bot's response message with acronym explanations.
        Progressive snark levels based on acronym count.
        
        Args:
            acronyms: List of acronym keys found in the comment
            
        Returns:
            Formatted response string
        """
        if not acronyms:
            return ""
        
        count = len(acronyms)
        
        # Progressive snark based on acronym count
        if count <= 3:
            response = "Hi! I detected a few acronyms in your comment:\n\n"
            footer = "^(I'm a bot that explains acronyms)"
        elif count <= 5:
            response = "Alright, let's decode this:\n\n"
            footer = "^(I'm a bot | Translating one comment at a time)"
        elif count <= 7:
            response = "Wow, someone loves their acronyms. Here's the translation:\n\n"
            footer = "^(I'm a bot | Because full words are too complicated to type out)"
        elif count <= 9:
            response = "Oh good, a comment that reads like military code. Let's decrypt this:\n\n"
            footer = "^(I'm a bot | My purpose is suffering through esoteric nonsense)"
        elif count <= 11:
            response = "*Deep breath* Okay. OKAY. Let's unpack this cryptic mess you've created:\n\n"
            footer = "^(I'm a bot | Someone please end my existence)"
        else:
            response = "ARE YOU KIDDING ME RIGHT NOW? Did you just have a stroke on your keyboard or are you genuinely trying to communicate? Fine. FINE. Here's your dissertation translated:\n\n"
            footer = "^(I'm a bot | This is my villain origin story | You did this)"
        
        # Add acronym explanations
        for acronym in acronyms:
            explanation = self.acronyms[acronym]
            response += f"- **{acronym}** - {explanation}\n"
        
        # Add footer
        response += "\n---\n"
        response += footer
        
        return response
    
    def should_skip_comment(self, comment) -> bool:
        """
        Determine if a comment should be skipped.
        
        Args:
            comment: PRAW comment object
            
        Returns:
            True if comment should be skipped, False otherwise
        """
        # Skip if already replied
        if comment.id in self.replied_comments:
            return True
        
        # Skip if it's our own comment
        if comment.author and comment.author.name == self.reddit.user.me().name:
            return True
        
        # Skip deleted/removed comments
        if comment.author is None:
            return True
        
        # Skip if comment is too short (less than 3 characters)
        if len(comment.body) < 3:
            return True
        
        return False
    
    def scan_subreddit(self, limit: int = 100):
        """
        Scan the subreddit for comments containing acronyms and respond.
        
        Args:
            limit: Maximum number of recent comments to check
        """
        logger.info(f"Starting scan of r/{self.subreddit_name}...")
        
        comments_processed = 0
        replies_sent = 0
        
        try:
            # Get recent comments from the subreddit
            for comment in self.subreddit.comments(limit=limit):
                comments_processed += 1
                
                # Skip if necessary
                if self.should_skip_comment(comment):
                    continue
                
                # Find acronyms in the comment
                found_acronyms = self.find_acronyms(comment.body)
                
                # Only reply if at least 2 acronyms are found
                if found_acronyms and len(found_acronyms) >= 2:
                    logger.info(f"Found acronyms {found_acronyms} in comment {comment.id}")
                    
                    # Format and send reply
                    response = self.format_response(found_acronyms)
                    
                    try:
                        comment.reply(response)
                        logger.info(f"Replied to comment {comment.id}")
                        
                        # Mark as replied
                        self.replied_comments.add(comment.id)
                        replies_sent += 1
                        
                        # Save state after each successful reply
                        self.save_replied_comments()
                        
                    except Exception as e:
                        logger.error(f"Failed to reply to comment {comment.id}: {e}")
            
            logger.info(f"Scan complete. Processed: {comments_processed}, Replied: {replies_sent}")
            
        except Exception as e:
            logger.error(f"Error during subreddit scan: {e}")
            raise
    
    def run(self):
        """Main execution method."""
        try:
            logger.info("=" * 50)
            logger.info("TowerAcronymBot started")
            logger.info("=" * 50)
            
            # Verify Reddit connection
            logger.info(f"Logged in as: u/{self.reddit.user.me().name}")
            
            # Run the scan
            self.scan_subreddit()
            
            logger.info("=" * 50)
            logger.info("TowerAcronymBot finished")
            logger.info("=" * 50)
            
        except Exception as e:
            logger.error(f"Bot execution failed: {e}")
            raise


def main():
    """Entry point for the bot."""
    try:
        bot = TowerAcronymBot()
        bot.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise


if __name__ == "__main__":
    main()
