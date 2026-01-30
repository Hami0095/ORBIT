import logging

logger = logging.getLogger(__name__)

class EmailService:
    async def send_email(self, to_email: str, subject: str, content: str) -> bool:
        logger.info(f"MOCK: Sending email to {to_email}: {subject}")
        return True

email_service = EmailService()
