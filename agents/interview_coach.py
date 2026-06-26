from typing import Any, Dict, List
from loguru import logger
from agents.base_agent import BaseAgent
from prompts.templates import INTERVIEW_COACH_PROMPT

class InterviewCoach(BaseAgent):
    """
    Agent responsible for simulating realistic technical and behavioral interviews.
    Keeps track of interview state and provides real-time feedback on user answers.
    """

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs a comprehensive evaluation on a completed interview session.
        
        Expected keys in input_data:
        - target_role: str
        - job_description: str
        - candidate_background: str
        - transcript: List[Dict[str, str]] (list of conversation turns)
        """
        target_role = input_data.get("target_role", "Software Engineer")
        job_description = input_data.get("job_description", "")
        candidate_background = input_data.get("candidate_background", "")
        transcript = input_data.get("transcript", [])

        if not transcript:
            logger.warning("InterviewCoach: Empty transcript provided for evaluation.")
            return {
                "success": False,
                "error": "Cannot evaluate an empty interview transcript."
            }

        logger.info(f"InterviewCoach: Evaluating session for role '{target_role}'...")
        
        # Combine transcript into readable text for prompt
        transcript_str = "\n".join([
            f"{turn.get('role', 'Speaker')}: {turn.get('content', '')}"
            for turn in transcript
        ])

        # Prepare evaluation prompt
        eval_prompt = (
            f"Here is a mock interview transcript for the role of '{target_role}'.\n"
            f"Job Description: {job_description}\n"
            f"Candidate Info: {candidate_background}\n\n"
            f"--- TRANSCRIPT ---\n{transcript_str}\n---\n\n"
            f"Please evaluate the candidate's performance, providing constructive critiques, "
            f"strengths, weaknesses, and a suggested overall score (0-100%)."
        )

        # Execute LLM call
        system_instruction = "You are a professional hiring manager and behavioral coach. Be strict, fair, and highly constructive."
        raw_feedback = self.llm.generate_text(eval_prompt, system_instruction=system_instruction)

        return {
            "success": True,
            "raw_feedback": raw_feedback,
            "scorecard": {
                "overall_score": 82.0, # Placeholder
                "communication_score": 85.0, # Placeholder
                "technical_score": 79.0, # Placeholder
                "key_strengths": [
                    "Strong use of the STAR framework for behavioral questions.",
                    "Excellent articulation of high-level architecture."
                ],
                "improvement_areas": [
                    "Needs to go deeper into edge cases during system design questions.",
                    "Pacing was slightly rushed in the mid-session."
                ]
            }
        }

    def generate_question(self, target_role: str, job_description: str, transcript: List[Dict[str, str]]) -> str:
        """
        Generates the next logical interview question based on the active conversation history.
        """
        logger.info(f"InterviewCoach: Generating next question for '{target_role}'...")
        
        # Render prompt based on template context
        prompt = self._render_prompt(
            INTERVIEW_COACH_PROMPT,
            target_role=target_role,
            job_description=job_description[:500] + "...",  # Truncate for prompt efficiency
            candidate_background="Candidate Profile",
            round_type="General Technical / Behavioral Mixed"
        )
        
        # Append conversation context
        transcript_context = "\n".join([f"{turn['role']}: {turn['content']}" for turn in transcript])
        full_prompt = f"{prompt}\n\nInterview History:\n{transcript_context}\n\nGenerate the next single interview question as the interviewer: "

        system_instruction = "You are an interviewer. Output ONLY the next question. Do not add metadata, commentary, or greetings."
        next_question = self.llm.generate_text(full_prompt, system_instruction=system_instruction)
        
        # Clean up output
        return next_question.strip()
