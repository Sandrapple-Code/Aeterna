from typing import Any, Dict
from loguru import logger
from agents.base_agent import BaseAgent


class ChatbotAgent(BaseAgent):
    """
    Agent for chatbot functionality
    """
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        user_message = input_data.get("message", "")
        
        # Mock response
        mock_response = f"Thanks for your message: '{user_message}'. I'm here to help with your career questions!"
        
        return {
            "success": True,
            "response": mock_response
        }
