"""
agents/chatbot_agent.py  –  Aeterna AI Career Coach
=====================================================
Uses Gemini multi-turn chat via generate_text_with_history().
The LLMService.client is explicitly injected by the page before this runs,
so the API key is guaranteed to be available.
"""

from typing import Any, Dict
from loguru import logger
from agents.base_agent import BaseAgent


class ChatbotAgent(BaseAgent):

    SYSTEM_INSTRUCTION = """You are Aeterna's expert AI career coach.

You have full context about this user: their education, interests, skills, goals,
recommended career path, roadmap timeline, and resume skill gaps.
Use ALL of this to give personalised, specific answers.

Critical rules:
- Answer the user's ACTUAL question. If they ask about AI/ML, answer about AI/ML.
  If they ask about cloud computing, answer about cloud. Never give off-topic advice.
- Name real tools, certifications, platforms, and companies relevant to their field.
- Be specific, structured, and encouraging.
- Format answers clearly with numbered steps or bullet points where helpful."""

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        user_message = input_data.get("message", "").strip()
        history      = input_data.get("history", [])
        user_context = input_data.get("user_context", {})

        if not user_message:
            return {"success": False, "response": "Please enter a message."}

        # Build Gemini-format conversation
        gemini_history = self._build_history(history, user_context)
        gemini_history.append({"role": "user", "content": user_message})

        logger.info(
            f"ChatbotAgent: {len(gemini_history)} turns → Gemini "
            f"| msg='{user_message[:60]}'"
        )

        # Try multi-turn method first
        response = None
        try:
            response = self.llm.generate_text_with_history(
                history=gemini_history,
                system_instruction=self.SYSTEM_INSTRUCTION,
            )
        except AttributeError:
            # Older LLMService without generate_text_with_history — fall back to generate_text
            logger.warning("ChatbotAgent: generate_text_with_history not found, using generate_text")
            flat_prompt = self._flatten_history(gemini_history)
            response = self.llm.generate_text(flat_prompt, system_instruction=self.SYSTEM_INSTRUCTION)

        if not response or "[MOCK RESPONSE]" in response or response.startswith("Error:"):
            logger.warning("ChatbotAgent: API not reachable — offline fallback.")
            response = self._offline_fallback(user_message, user_context)

        return {"success": True, "response": response}

    # ── helpers ──────────────────────────────────────────────────────────────

    def _build_history(self, history: list, user_context: dict) -> list:
        gemini_history = []

        # Prepend profile context as first exchange
        ctx = self._format_context(user_context)
        if ctx:
            gemini_history.append({"role": "user", "content": ctx})
            gemini_history.append({
                "role": "model",
                "content": (
                    "I have your full profile. I'll use your interests, skills, goals, "
                    "and career analysis to give you personalised advice. What would you like to know?"
                ),
            })

        # Append prior turns (last 20, converting "assistant" → "model")
        for msg in history[-20:]:
            role = "model" if msg.get("role") == "assistant" else "user"
            gemini_history.append({"role": role, "content": msg.get("content", "")})

        return gemini_history

    def _format_context(self, user_context: dict) -> str:
        if not user_context:
            return ""
        lines = ["[USER PROFILE & CAREER ANALYSIS]"]
        intake = user_context.get("intake_data", {})
        if intake:
            lines += [
                f"Education: {intake.get('education', 'N/A')}",
                f"Stage: {intake.get('current_year', 'N/A')}",
                f"Interests: {intake.get('interests', 'N/A')}",
                f"Skills: {intake.get('skills', 'N/A')}",
                f"Work Style: {intake.get('work_style', 'N/A')}",
                f"Goals: {intake.get('goals', 'N/A')}",
            ]
        analysis = user_context.get("analysis_result") or {}
        disc = analysis.get("discovery", {})
        if disc.get("success"):
            rec = disc.get("career_matches", {}).get("recommended_career", "")
            if rec:
                lines.append(f"AI-Recommended Career: {rec}")
        planner = analysis.get("planner", {})
        if planner.get("success"):
            rm = planner.get("roadmap", {})
            lines.append(f"Roadmap Timeline: {rm.get('estimated_timeline', 'N/A')}")
            lines.append(f"Readiness Score: {rm.get('career_readiness_score', 'N/A')}%")
        resume = (analysis.get("resume") or {})
        if resume.get("success"):
            ins = resume.get("structured_insights", {})
            lines.append(f"Resume Match Score: {ins.get('match_score', 'N/A')}%")
            gaps = ins.get("skill_gaps_identified", [])
            if gaps:
                lines.append(f"Resume Gaps: {', '.join(gaps[:5])}")
        return "\n".join(lines) if len(lines) > 1 else ""

    def _flatten_history(self, history: list) -> str:
        """Fallback: flatten history to a single prompt string."""
        parts = []
        for msg in history:
            role = "Assistant" if msg["role"] == "model" else "User"
            parts.append(f"{role}: {msg['content']}")
        parts.append("Assistant:")
        return "\n".join(parts)

    def _offline_fallback(self, message: str, ctx: dict) -> str:
        intake    = (ctx or {}).get("intake_data", {})
        interests = intake.get("interests", "your field")
        return (
            f"⚠️ **Offline Mode** — Gemini API is not reachable.\n\n"
            f"Please check that your Gemini API key is entered under ⚙️ **Settings**. "
            f"The green '✅ Gemini API connected' banner on this page confirms the key is active.\n\n"
            f"Once connected, I can answer your question about *\"{message}\"* "
            f"with full personalised advice for **{interests}**."
        )