import logging

logger = logging.getLogger(__name__)

class SlackService:
    async def send_message(self, channel: str, text: str) -> bool:
        logger.info(f"MOCK: Sending Slack message to {channel}: {text}")
        return True

slack_service = SlackService()
