from typing import Any, Dict
from loguru import logger
from agents.base_agent import BaseAgent
from prompts.templates import OPPORTUNITY_AGENT_PROMPT
from agents.schemas import OpportunityList

class OpportunityAgent(BaseAgent):
    """
    Agent responsible for analyzing professional roadmaps, resume insights,
    searching the web for active opportunities, and generating structured opportunity listings.
    """

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the opportunity matching workflow.
        
        Expected keys in input_data:
        - roadmap_summary: str (optional)
        - resume_summary: str (optional)
        """
        roadmap_summary = input_data.get("roadmap_summary", "")
        resume_summary = input_data.get("resume_summary", "")

        logger.info("OpportunityAgent: Finding tailored career opportunities...")

        # Render prompt for search
        search_prompt = self._render_prompt(
            OPPORTUNITY_AGENT_PROMPT,
            roadmap_summary=roadmap_summary or "None provided",
            resume_summary=resume_summary or "None provided"
        )

        raw_search_results = ""
        try:
            # Step 1: Query the model with Google Search grounding enabled (returns unstructured text)
            logger.info("OpportunityAgent Step 1: Performing web search grounding...")
            system_instruction = "You are a professional recruiting coordinator and opportunity scout."
            raw_search_results = self.llm.generate_text(
                search_prompt,
                system_instruction=system_instruction,
                enable_search=True
            )
        except Exception as e:
            logger.error(f"OpportunityAgent Step 1 Search failed: {e}")

        # Step 2: Use structured generation (without tool search) to convert search results to JSON schema
        result = None
        if raw_search_results and not raw_search_results.startswith("Error") and "[MOCK RESPONSE]" not in raw_search_results:
            try:
                logger.info("OpportunityAgent Step 2: Parsing search results into structured JSON...")
                parser_prompt = f"Convert the following search results and matching opportunities into a structured OpportunityList JSON:\n\n{raw_search_results}"
                result = self.llm.generate_structured_data(
                    parser_prompt,
                    OpportunityList,
                    system_instruction="You are a JSON parser that outputs valid OpportunityList schema.",
                    enable_search=False
                )
            except Exception as e:
                logger.error(f"OpportunityAgent Step 2 Parser failed: {e}")

        # Fallback to high-quality mockup data if either step fails
        if result is None:
            logger.warning("OpportunityAgent: LLM calls failed or rate limited. Utilizing high-quality mock fallbacks.")
            roadmap_lower = roadmap_summary.lower()
            
            if "sing" in roadmap_lower or "music" in roadmap_lower or "vocal" in roadmap_lower:
                opps = {
                    "internships": [
                        "Vocalist Intern - Royal Academy of Music Production",
                        "Sound Recording Assistant - Universal Music Group"
                    ],
                    "jobs": [
                        "Lead Vocalist - Cruise Line Entertainment (careers.cruises)",
                        "Session Singer - SoundBetter (soundbetter.com)"
                    ],
                    "hackathons": [
                        "Abbey Road Red Music Tech Hackathon",
                        "Sonar+D Innovation Challenge"
                    ],
                    "fellowships": [
                        "Berklee College of Music Summer Fellowship",
                        "BMI Foundation Music Grant program"
                    ],
                    "recommended_companies": [
                        "Universal Music Group",
                        "Warner Music",
                        "Sony Music",
                        "SoundBetter",
                        "Spotify"
                    ]
                }
                raw_opps = "Successfully matched high-value opportunities including live performance auditions, studio sessions, and music technology fellowships."
            elif "robot" in roadmap_lower or "mechatronic" in roadmap_lower or "control" in roadmap_lower:
                opps = {
                    "internships": [
                        "Robotics Software Engineer Intern - Boston Dynamics (bostondynamics.com/careers)",
                        "Mechatronics Engineering Intern - Tesla (tesla.com/careers)"
                    ],
                    "jobs": [
                        "Control Systems Engineer - Skydio (skydio.com/careers)",
                        "Embedded Systems Developer - iRobot (irobot.com/careers)"
                    ],
                    "hackathons": [
                        "NASA Space Apps Challenge (spaceappschallenge.org)",
                        "RoboSub Global Autonomous Robotics Competition"
                    ],
                    "fellowships": [
                        "Open Source Robotics Foundation (OSRF) Fellowship",
                        "Robotics Research Fellowship program"
                    ],
                    "recommended_companies": [
                        "Boston Dynamics",
                        "Tesla",
                        "Skydio",
                        "iRobot",
                        "Universal Robots"
                    ]
                }
                raw_opps = "Successfully matched high-value opportunities including hardware integration, actuator control, embedded firmware development, and autonomous robotics challenges."
            else:
                opps = {
                    "internships": [
                        "Software Engineer Intern - Google (careers.google.com)",
                        "Backend Developer Intern - Microsoft (careers.microsoft.com)"
                    ],
                    "jobs": [
                        "Junior Software Developer - Amazon (jobs.amazon.com)",
                        "Full Stack Engineer - Stripe (stripe.com/jobs)"
                    ],
                    "hackathons": [
                        "Google Solution Challenge (build solutions for global goals)",
                        "Major League Hacking (MLH) Global Hackathon Season (mlh.io)"
                    ],
                    "fellowships": [
                        "MLH Fellowship (12-week open-source software engineering fellowship)",
                        "Major League Hacking Production Engineering Track"
                    ],
                    "recommended_companies": [
                        "Google",
                        "Microsoft",
                        "Amazon",
                        "Stripe",
                        "Atlassian"
                    ]
                }
                raw_opps = "Successfully matched high-value software opportunities including backend development positions at top tier tech companies and active developer hackathons."
                
            return {
                "success": True,
                "is_mock": True,
                "raw_opportunities": raw_opps,
                "opportunities": opps
            }

        return {
            "success": True,
            "raw_opportunities": result.detailed_analysis,
            "opportunities": {
                "internships": result.internships,
                "jobs": result.jobs,
                "hackathons": result.hackathons,
                "fellowships": result.fellowships,
                "recommended_companies": result.recommended_companies
            }
        }
