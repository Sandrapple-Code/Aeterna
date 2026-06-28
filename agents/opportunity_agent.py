"""
agents/opportunity_agent.py  –  Aeterna Opportunity Scout
==========================================================
Finds REAL, PERSONALISED opportunities using Gemini web-grounded search.
The user's actual interests / skills / goals drive every prompt.
"""

from typing import Any, Dict
from loguru import logger
from agents.base_agent import BaseAgent
from agents.schemas import OpportunityList


class OpportunityAgent(BaseAgent):

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        input_data keys:
          interests          – user's stated interests (REQUIRED for personalisation)
          skills             – user's stated skills
          goals              – user's career goals
          recommended_career – career recommended by CareerDiscoveryAgent
          roadmap_summary    – text from CareerPathfinder (optional context)
          resume_summary     – text from ResumeOptimizer (optional context)
        """
        interests          = (input_data.get("interests") or "").strip()
        skills             = (input_data.get("skills") or "").strip()
        goals              = (input_data.get("goals") or "").strip()
        recommended_career = (input_data.get("recommended_career") or "").strip()
        roadmap_summary    = (input_data.get("roadmap_summary") or "").strip()
        resume_summary     = (input_data.get("resume_summary") or "").strip()

        focus = interests or recommended_career or "general tech"

        logger.info(
            f"OpportunityAgent: interests='{interests}' | "
            f"skills='{skills[:40]}' | career='{recommended_career}'"
        )

        # ── Step 1: Web-grounded search ───────────────────────────────────────
        search_prompt = self._build_search_prompt(
            interests, skills, goals, recommended_career,
            roadmap_summary, resume_summary
        )

        system_search = (
            "You are a specialised recruiting coordinator. "
            "Search the web and return SPECIFIC, CURRENT opportunities. "
            "Every single result MUST match the user's stated field of interest. "
            "Do NOT return generic software engineering jobs if the user is "
            "interested in cloud computing, finance, robotics, design, music, etc."
        )

        raw = ""
        try:
            logger.info("OpportunityAgent Step-1: web-grounded search...")
            raw = self.llm.generate_text(
                search_prompt,
                system_instruction=system_search,
                enable_search=True,
            )
            logger.info(f"Step-1 result: {len(raw)} chars")
        except Exception as e:
            logger.error(f"OpportunityAgent Step-1 failed: {e}")

        # ── Step 2: Parse into structured JSON ────────────────────────────────
        result = None
        if raw and "[MOCK RESPONSE]" not in raw and not raw.startswith("Error"):
            parse_prompt = (
                f"User interests: {interests}\n"
                f"User skills: {skills}\n"
                f"Target career: {recommended_career}\n\n"
                f"Convert the following search results into an OpportunityList JSON. "
                f"All items MUST be relevant to '{focus}'. "
                f"Do NOT include generic software jobs if the focus is something else.\n\n"
                f"Search results:\n{raw}"
            )
            try:
                logger.info("OpportunityAgent Step-2: parsing into structured JSON...")
                result = self.llm.generate_structured_data(
                    parse_prompt,
                    OpportunityList,
                    system_instruction=(
                        "Output a valid OpportunityList JSON. "
                        "Every opportunity must match the user's specific interests."
                    ),
                )
            except Exception as e:
                logger.error(f"OpportunityAgent Step-2 failed: {e}")

        if result is not None:
            logger.info("OpportunityAgent: Gemini returned personalised opportunities.")
            return {
                "success": True,
                "is_mock": False,
                "raw_opportunities": result.detailed_analysis,
                "opportunities": {
                    "jobs":                  result.jobs,
                    "internships":           result.internships,
                    "hackathons":            result.hackathons,
                    "fellowships":           result.fellowships,
                    "recommended_companies": result.recommended_companies,
                },
            }

        # ── Fallback: honest, field-aware placeholder ─────────────────────────
        logger.warning(
            f"OpportunityAgent: Gemini unavailable – generating "
            f"field-aware fallback for '{focus}'."
        )
        return self._field_aware_fallback(focus, interests, skills, recommended_career)

    # ── helpers ──────────────────────────────────────────────────────────────

    def _build_search_prompt(
        self, interests, skills, goals, recommended_career,
        roadmap_summary, resume_summary
    ) -> str:
        return f"""Find current, real-world career opportunities specifically for this person:

INTERESTS: {interests or 'Not specified'}
SKILLS: {skills or 'Not specified'}
CAREER GOALS: {goals or 'Not specified'}
TARGET CAREER: {recommended_career or 'Not yet determined'}
CAREER ROADMAP CONTEXT: {roadmap_summary[:500] if roadmap_summary else 'N/A'}
RESUME INSIGHTS: {resume_summary[:300] if resume_summary else 'N/A'}

SEARCH INSTRUCTIONS:
1. Find ACTIVE job postings that match the user's interests ({interests or recommended_career}).
2. Find OPEN internship applications relevant to their field.
3. Find UPCOMING hackathons or competitions in their domain.
4. Find fellowships or grants applicable to their area.
5. Recommend companies specifically known for work in: {interests or recommended_career}.

CRITICAL: If the user is interested in Cloud Computing → return cloud/DevOps/AWS/GCP roles.
If Finance → return fintech/banking/quant roles. If Robotics → robotics/embedded roles.
Do NOT give generic Python/web-dev results unless that is the explicit interest.

Search the web now for the most current listings."""

    def _field_aware_fallback(
        self, focus: str, interests: str, skills: str, recommended_career: str
    ) -> Dict[str, Any]:
        """
        Honest fallback that tells the user WHERE to search for their specific field,
        rather than returning hardcoded irrelevant listings.
        """
        field = focus.split(",")[0].strip()
        career = recommended_career or f"{field} professional"

        return {
            "success": True,
            "is_mock": True,
            "raw_opportunities": (
                f"Offline mode: showing search guidance for '{field}'. "
                f"Connect your Gemini API key for live web-searched results."
            ),
            "opportunities": {
                "jobs": [
                    f"Search LinkedIn Jobs → '{field}' → filter by 'Entry level' or 'Internship'",
                    f"Search Indeed → '{career}' → sort by date (last 7 days)",
                    f"Search Glassdoor → '{field} jobs' → filter by company rating 4+",
                ],
                "internships": [
                    f"Search Internshala → '{field} internship'",
                    f"Search LinkedIn → '{field} intern' → filter 'Internship' job type",
                    f"Check university placement portal for '{field}' openings",
                ],
                "hackathons": [
                    f"Devpost.com → search '{field}' → filter by upcoming",
                    "MLH (mlh.io) → open to all technical disciplines",
                    f"Unstop.com → search '{field} hackathon'",
                ],
                "fellowships": [
                    f"Search Idealist.org → '{field} fellowship'",
                    "Google Summer of Code → open source projects across all fields",
                    f"Search LinkedIn → '{field} fellowship 2025'",
                ],
                "recommended_companies": [
                    f"Search LinkedIn → 'Companies hiring {career}' → follow top results",
                    f"Glassdoor → 'Best companies for {field} professionals'",
                    f"AngelList/Wellfound → filter by '{field}' industry tag",
                ],
            },
        }