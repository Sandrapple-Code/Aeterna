from typing import Any, Dict
from loguru import logger
from agents.base_agent import BaseAgent
from prompts.templates import CAREER_DISCOVERY_PROMPT
from agents.schemas import CareerDiscoveryOutput

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
        result = self.llm.generate_structured_data(
            prompt,
            CareerDiscoveryOutput,
            system_instruction=system_instruction
        )

        if result is None:
            logger.warning("CareerDiscoveryAgent: API call failed or rate limited. Using high-quality mock fallback data.")
            interest_word = interests.split(',')[0].strip() if interests else "Technology"
            interest_lower = interest_word.lower()
            
            if "sing" in interest_lower or "music" in interest_lower:
                recommended = "Professional Singer"
                raw_analysis = f"Based on your creative background in {education or 'your studies'} and strong interests in {interests}, you are well-suited to pursue a path as a **{recommended}**. We recommend focusing on vocal range development, stage presence, and digital music production."
                matches = [
                    {
                        "title": "Professional Singer / Vocalist",
                        "fit_reason": f"Completely aligns with your creative interest in '{interests}' and goals of '{goals or 'artistic expression'}'.",
                        "industry_demand": "Moderate (highly competitive)",
                        "learning_curve": "High"
                    },
                    {
                        "title": "Music Producer / Sound Designer",
                        "fit_reason": f"Complements your interest in music with commercial audio editing skills.",
                        "industry_demand": "Moderate-High",
                        "learning_curve": "Moderate"
                    }
                ]
            elif "robot" in interest_lower or "mechatronic" in interest_lower:
                recommended = "Robotics & Mechatronics Engineer"
                raw_analysis = f"Based on your technical background in {education or 'your studies'} and interests in {interests}, you are well-positioned for roles in **{recommended}**. Focus on C++, ROS, control theory, and hardware prototyping."
                matches = [
                    {
                        "title": "Robotics & Mechatronics Engineer",
                        "fit_reason": f"Matches your goals of '{goals or 'professional growth'}' and skills in {skills or 'problem-solving'}.",
                        "industry_demand": "High (growing at 35% YoY)",
                        "learning_curve": "High"
                    },
                    {
                        "title": "Embedded Systems Developer",
                        "fit_reason": f"Leverages your foundational skills in hardware integration and programming.",
                        "industry_demand": "Very High",
                        "learning_curve": "Moderate-High"
                    }
                ]
            else:
                recommended = f"{interest_word} Specialist"
                raw_analysis = f"Based on your background in {education or 'your studies'} and interests in {interests}, we recommend the path of **{recommended}**. You should focus on building core domain expertise and practical project work.",
                matches = [
                    {
                        "title": recommended,
                        "fit_reason": f"Matches your goals of '{goals or 'professional growth'}' and skills in {skills or 'core competencies'}.",
                        "industry_demand": "High",
                        "learning_curve": "Moderate"
                    },
                    {
                        "title": "Project Coordinator",
                        "fit_reason": f"Aligns with your preferred work style: '{work_style or 'Collaborative'}' and foundational skills.",
                        "industry_demand": "Moderate-High",
                        "learning_curve": "Low-Moderate"
                    }
                ]
            
            return {
                "success": True,
                "is_mock": True,
                "raw_analysis": raw_analysis,
                "career_matches": {
                    "recommended_career": recommended,
                    "top_matches": matches
                }
            }

        # Return structured matches alongside raw text
        return {
            "success": True,
            "raw_analysis": result.detailed_analysis,
            "career_matches": {
                "recommended_career": result.recommended_career,
                "top_matches": [m.model_dump() for m in result.top_matches]
            }
        }
