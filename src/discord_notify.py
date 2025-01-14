import os
import time
import random
import requests
from typing import Dict

class DiscordNotifier:
    def __init__(self):
        self.webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        if not self.webhook_url:
            raise ValueError("DISCORD_WEBHOOK_URL environment variable not set")
        self.rate_limit_remaining = 5
        self.rate_limit_reset = 0

    # def _get_random_header_emoji(self) -> str:
    #     return random.choice(['🧪', '🔬', '🧠', '🌟', '⚗️', '🔮', '📊', '🎯', '💫', '🌈'])

    def _get_shuffled_header_emojis(self) -> str:
        """Get all psychedelic-themed emojis in a random order."""
        emojis = ['⚛️', '🌿', '🌵', '🍄']
        random.shuffle(emojis)
        return ''.join(emojis)


    def _get_location_emoji(self, location: str) -> str:
        """Get region-appropriate emoji based on location text."""
        if any(x in location.lower() for x in ['uk', 'london', 'england', 'britain']):
            return '🇬🇧'
        if any(x in location.lower() for x in ['usa', 'united states', 'america']):
            return '🇺🇸'
        if 'canada' in location.lower():
            return '🇨🇦'
        if any(x in location.lower() for x in ['australia', 'sydney', 'melbourne']):
            return '🇦🇺'
        return '🌍'

    def format_study_message(self, study: Dict) -> str:
        header_emojis = self._get_shuffled_header_emojis()
        reversed_header_emojis = ''.join(reversed(header_emojis))  
        project_name = study.get('atlas-research_project_name', '')
        location_text = study.get('atlas-location_text', 'N/A')
        location_emoji = self._get_location_emoji(location_text)
        
        recruiting_status = '✅ Yes' if study.get('recruiting') else '❌ No'
        
        if project_name and project_name != study['post_title']:
            project_name = f"📝 **Project Name:** {project_name}\n"
        else:
            project_name = ""
            
        return (
            f"🚨 {header_emojis} 🚨 **New Psychedelic Study Found**  🚨 {reversed_header_emojis} 🚨\n\n"
            f"📑 **Title:** {study['post_title']}\n"
            f"{project_name}"
            f"🎯 **Research Theme:** {study.get('atlas-summary_research_theme', 'N/A')}\n"
            f"📋 **Type:** {study.get('atlas-type_of_research', 'N/A')}\n"
            f"{location_emoji} **Location:** {location_text}\n"
            f"👥 **Recruiting:** {recruiting_status}\n"
            f"\n🔗 *Learn more at https://atlasofpsychedelicresearch.com*"
        )

    def send_notification(self, study: Dict) -> None:
        message = self.format_study_message(study)
        payload = {"content": message}
        
        # Check rate limits
        current_time = time.time()
        if current_time < self.rate_limit_reset:
            sleep_time = self.rate_limit_reset - current_time + 0.1
            time.sleep(sleep_time)
        
        response = requests.post(
            self.webhook_url,
            json=payload
        )
        
        # Handle rate limits
        if response.status_code == 429:
            retry_after = float(response.headers.get('X-RateLimit-Reset-After', 5))
            self.rate_limit_reset = time.time() + retry_after
            time.sleep(retry_after)
            # Retry the request
            response = requests.post(
                self.webhook_url,
                json=payload
            )
        
        # Update rate limit info from headers
        self.rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', 5))
        reset_after = float(response.headers.get('X-RateLimit-Reset-After', 0))
        if reset_after > 0:
            self.rate_limit_reset = time.time() + reset_after
        
        response.raise_for_status()

# import os
# import time
# import requests
# from typing import Dict

# class DiscordNotifier:
#     def __init__(self):
#         self.webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
#         if not self.webhook_url:
#             raise ValueError("DISCORD_WEBHOOK_URL environment variable not set")
#         self.rate_limit_remaining = 5
#         self.rate_limit_reset = 0

#     def format_study_message(self, study: Dict) -> str:
#         project_name = study['atlas-research_project_name']
#         if project_name != study['post_title']:
#             project_name = f"**Project Name:** {project_name}\n"
#         else:
#             project_name = ""
#         return (
#             f"🔬 **New Study Added**\n\n"
#             f"**Title:** {study['post_title']}\n"
#             f"{project_name}"
#             f"**Research Theme:** {study.get('atlas-summary_research_theme', 'N/A')}\n"
#             f"**Type:** {study.get('atlas-type_of_research', 'N/A')}\n"
#             f"**Location:** {study.get('atlas-location_text', 'N/A')}\n"
#             f"**Recruiting:** {'Yes' if study.get('recruiting') else 'No'}\n"
#         )

#     def send_notification(self, study: Dict) -> None:
#         message = self.format_study_message(study)
#         payload = {"content": message}
        
#         # Check rate limits
#         current_time = time.time()
#         if current_time < self.rate_limit_reset:
#             sleep_time = self.rate_limit_reset - current_time + 0.1
#             time.sleep(sleep_time)
        
#         response = requests.post(
#             self.webhook_url,
#             json=payload
#         )
        
#         # Handle rate limits
#         if response.status_code == 429:
#             retry_after = float(response.headers.get('X-RateLimit-Reset-After', 5))
#             self.rate_limit_reset = time.time() + retry_after
#             time.sleep(retry_after)
#             # Retry the request
#             response = requests.post(
#                 self.webhook_url,
#                 json=payload
#             )
        
#         # Update rate limit info from headers
#         self.rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', 5))
#         reset_after = float(response.headers.get('X-RateLimit-Reset-After', 0))
#         if reset_after > 0:
#             self.rate_limit_reset = time.time() + reset_after
        
#         response.raise_for_status()