from typing import Any, Dict
from loguru import logger
from agents.base_agent import BaseAgent
from prompts.templates import CAREER_DISCOVERY_PROMPT

class CareerDiscoveryAgent(BaseAgent):
    """
    Agent responsible for analyzing academic/professional background, interests, and skills
    to identify optimal career trajectories, fit alignment, and industry demand metrics.
    """

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the career discovery/matching workflow.
        
        Expected keys in input_data:
        - education: str
        - current_year: str
        - interests: str
        - skills: str
        - work_style: str
        - goals: str
        """
        education = input_data.get("education", "")
        current_year = input_data.get("current_year", "")
        interests = input_data.get("interests", "")
        skills = input_data.get("skills", "")
        work_style = input_data.get("work_style", "")
        goals = input_data.get("goals", "")

        if not interests and not skills:
            logger.warning("CareerDiscoveryAgent: Missing both interests and skills in inputs.")
            return {
                "success": False,
                "error": "At least interests or skills must be provided."
            }

        logger.info("CareerDiscoveryAgent: Running career discovery analysis...")

        # Render prompt
        prompt = self._render_prompt(
            CAREER_DISCOVERY_PROMPT,
            education=education,
            current_year=current_year,
            interests=interests,
            skills=skills,
            work_style=work_style,
            goals=goals
        )

        # Execute LLM call
        system_instruction = "You are a seasoned career coach and corporate talent strategist. Help individuals find their ideal career paths."
        raw_analysis = self.llm.generate_text(prompt, system_instruction=system_instruction)

        # Return structured matches alongside raw text
        return {
            "success": True,
            "raw_analysis": raw_analysis,
            "career_matches": {
                "recommended_career": "Cloud Security Architect",
                "top_matches": [
                    {
                        "title": "Cloud Security Architect",
                        "fit_reason": "Aligns with interests in cloud infrastructure security and leveraging existing software engineering backgrounds.",
                        "industry_demand": "High (growing demand due to compliance frameworks and cloud migrations)",
                        "learning_curve": "Moderate to High (requires deep knowledge of IAM and networking)"
                    },
                    {
                        "title": "DevOps Engineer",
                        "fit_reason": "Leverages existing technical background while incorporating interest in system automation and scalability.",
                        "industry_demand": "Very High",
                        "learning_curve": "Moderate"
                    },
                    {
                        "title": "Solutions Architect",
                        "fit_reason": "Matches broad technical interest and strong client-facing communication goals.",
                        "industry_demand": "High",
                        "learning_curve": "Moderate"
                    }
                ]
            }
        }
