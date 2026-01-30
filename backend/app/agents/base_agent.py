from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgent(ABC):
    @abstractmethod
    async def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        pass
