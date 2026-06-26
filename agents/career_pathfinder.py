from typing import Any, Dict
from loguru import logger
from agents.base_agent import BaseAgent
from prompts.templates import CAREER_PATHFINDER_PROMPT

class CareerPathfinder(BaseAgent):
    """
    Agent responsible for designing professional transition roadmaps,
    identifying core skill gaps, and mapping milestones from current roles to target roles.
    """

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the career path mapping workflow.
        
        Expected keys in input_data:
        - current_role: str
        - target_destination: str
        - skill_profile: str (comma separated or description)
        """
        current_role = input_data.get("current_role", "")
        target_destination = input_data.get("target_destination", "")
        skill_profile = input_data.get("skill_profile", "")

        if not current_role or not target_destination:
            logger.warning("CareerPathfinder: Missing current_role or target_destination in inputs.")
            return {
                "success": False,
                "error": "Both current_role and target_destination are required."
            }

        logger.info(f"CareerPathfinder: Mapping transition path from '{current_role}' to '{target_destination}'...")

        # Render prompt
        prompt = self._render_prompt(
            CAREER_PATHFINDER_PROMPT,
            current_role=current_role,
            target_destination=target_destination,
            skill_profile=skill_profile
        )

        # Execute LLM call
        system_instruction = "You are a senior talent strategist and corporate organizational architect. Give structured, actionable advice."
        roadmap_analysis = self.llm.generate_text(prompt, system_instruction=system_instruction)

        # Return structured progression roadmap alongside raw text
        return {
            "success": True,
            "raw_analysis": roadmap_analysis,
            "roadmap": {
                "estimated_timeline": "12-18 Months",
                "phases": [
                    {
                        "phase_number": 1,
                        "title": "Foundation & Core Upskilling",
                        "duration": "0-6 Months",
                        "objectives": [
                            f"Acquire primary technical stack required for {target_destination}",
                            "Build 2 portfolio-grade projects illustrating foundational competency."
                        ]
                    },
                    {
                        "phase_number": 2,
                        "title": "Bridging Experience",
                        "duration": "6-12 Months",
                        "objectives": [
                            "Undertake cross-functional assignments in current organization.",
                            "Acquire intermediate industry certifications."
                        ]
                    },
                    {
                        "phase_number": 3,
                        "title": "Market Positioning & Target Application",
                        "duration": "12-18 Months",
                        "objectives": [
                            f"Tailor professional profiles specifically to {target_destination} specifications.",
                            "Initiate active applications and target networking campaigns."
                        ]
                    }
                ]
            }
        }
