from abc import ABC, abstractmethod
from typing import Any, Dict
from loguru import logger
from services.llm_service import LLMService
from services.db_service import DBService

class BaseAgent(ABC):
    """
    Abstract Base Class for all CareerForge Engine AI Agents.
    Enforces unified interfaces for LLM and DB service injection.
    """

    def __init__(self, llm_service: LLMService, db_service: DBService) -> None:
        self.llm = llm_service
        self.db = db_service
        logger.info(f"Agent [{self.__class__.__name__}] initialized.")

    @abstractmethod
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the agent's core cognitive process.
        Must be implemented by subclasses.
        """
        pass

    def _render_prompt(self, template: str, **kwargs: Any) -> str:
        """
        Helper method to format a prompt template with keyword arguments.
        """
        try:
            return template.format(**kwargs)
        except KeyError as e:
            logger.error(f"Failed to format prompt template due to missing key: {e}")
            raise e
