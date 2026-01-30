import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class CalendarService:
    async def schedule_event(self, summary: str, start_time: datetime, end_time: datetime) -> str:
        event_id = "event_123"
        logger.info(f"MOCK: Scheduling calendar event: {summary} at {start_time}")
        return event_id

calendar_service = CalendarService()
