from typing import Any, Dict
from loguru import logger
from agents.base_agent import BaseAgent
from prompts.templates import CAREER_PATHFINDER_PROMPT
from agents.schemas import CareerRoadmap

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
        - recommended_career: str (optional)
        - resume_skill_gaps: str (optional)
        """
        current_role = input_data.get("current_role", "")
        target_destination = input_data.get("target_destination", "")
        skill_profile = input_data.get("skill_profile", "")
        recommended_career = input_data.get("recommended_career", "")
        resume_skill_gaps = input_data.get("resume_skill_gaps", "")

        if not current_role or not target_destination:
            logger.warning("CareerPathfinder: Missing current_role or target_destination in inputs.")
            return {
                "success": False,
                "error": "Both current_role and target_destination are required.",
                "raw_analysis": None,
                "roadmap": None
            }

        logger.info(f"CareerPathfinder: Mapping transition path from '{current_role}' to '{target_destination}'...")

        # Render prompt
        prompt = self._render_prompt(
            CAREER_PATHFINDER_PROMPT,
            current_role=current_role,
            target_destination=target_destination,
            skill_profile=skill_profile,
            recommended_career=recommended_career or target_destination,
            resume_skill_gaps=resume_skill_gaps or "None identified"
        )

        # Execute LLM call
        system_instruction = "You are a senior talent strategist and corporate organizational architect. Give structured, actionable advice."
        result = self.llm.generate_structured_data(
            prompt,
            CareerRoadmap,
            system_instruction=system_instruction
        )

        if result is None:
            logger.warning("CareerPathfinder: API call failed. Using mock career roadmap.")
            target_lower = target_destination.lower()
            
            if "ai" in target_lower or "machine learning" in target_lower or "ml " in target_lower or "data science" in target_lower:
                timeline = "3.5 - 5 Years"
                score = 35.0
                phases = [
                    {
                        "phase_number": 1,
                        "title": "Mathematics, Probability & Python Foundations",
                        "duration": "12 Months",
                        "objectives": ["Master Linear Algebra, Multivariable Calculus, and Probability Theory", "Become fluent in Python, NumPy, Pandas, and Matplotlib"]
                    },
                    {
                        "phase_number": 2,
                        "title": "Classical Machine Learning & Feature Engineering",
                        "duration": "12 Months",
                        "objectives": ["Learn Scikit-Learn models: Regressions, Tree-based models, and SVMs", "Implement cross-validation, feature scaling, and dimensional reductions (PCA)"]
                    },
                    {
                        "phase_number": 3,
                        "title": "Deep Learning & Neural Architectures",
                        "duration": "12 Months",
                        "objectives": ["Build and train neural networks using PyTorch or TensorFlow", "Learn Convolutional Networks (CNNs) for vision and Transformers/LSTMs for NLP"]
                    },
                    {
                        "phase_number": 4,
                        "title": "MLOps, Model Deployment & Scale",
                        "duration": "12 Months",
                        "objectives": ["Deploy models using FastAPI and containerize via Docker", "Implement CI/CD pipeline automation and monitor drift using MLflow"]
                    },
                    {
                        "phase_number": 5,
                        "title": "Advanced Capstone & Professional Portfolio",
                        "duration": "12 Months",
                        "objectives": ["Build and publish an end-to-end AI project on GitHub", "Prepare for rigorous ML engineering coding and architecture interviews"]
                    }
                ]
            elif "robot" in target_lower or "mechatronic" in target_lower or "control" in target_lower:
                timeline = "2.5 - 4 Years"
                score = 30.0
                phases = [
                    {
                        "phase_number": 1,
                        "title": "Embedded Systems & Firmware Foundation",
                        "duration": "12 Months",
                        "objectives": ["Master C/C++ programming for microcontrollers", "Study circuit analysis, analog/digital design, and PCB layouts"]
                    },
                    {
                        "phase_number": 2,
                        "title": "Robotics Operating System (ROS) & Kinematics",
                        "duration": "12 Months",
                        "objectives": ["Build nodes, publish topics, and write launch files in ROS/ROS2", "Master forward and inverse kinematics of multi-joint arms"]
                    },
                    {
                        "phase_number": 3,
                        "title": "Control Systems Theory & Sensors Integration",
                        "duration": "12 Months",
                        "objectives": ["Integrate LIDAR, IMU, ultrasonic, and camera sensors", "Implement closed-loop control algorithms (PID, Kalman Filters) in firmware"]
                    },
                    {
                        "phase_number": 4,
                        "title": "Autonomous Navigation & Hardware Synthesis",
                        "duration": "12 Months",
                        "objectives": ["Deploy SLAM and path planning (A*, Dijkstra) on custom chassis", "Build a physical 3-axis robot or arm prototype and perform system calibration"]
                    }
                ]
            elif "sing" in target_lower or "music" in target_lower or "vocal" in target_lower:
                timeline = "2 - 3 Years"
                score = 25.0
                phases = [
                    {
                        "phase_number": 1,
                        "title": "Vocal Technique & Range Extension",
                        "duration": "8 Months",
                        "objectives": ["Practice daily vocal exercises and breath support technique", "Identify vocal range and perform ear training exercises"]
                    },
                    {
                        "phase_number": 2,
                        "title": "Music Theory & Instrumental Accompaniment",
                        "duration": "8 Months",
                        "objectives": ["Master basic music theory, sight-reading, and rhythm", "Learn foundational keyboard or acoustic guitar for song accompaniment"]
                    },
                    {
                        "phase_number": 3,
                        "title": "Live Performance & Stage Presence",
                        "duration": "10 Months",
                        "objectives": ["Perform regularly at open mics, local venues, and ensembles", "Learn mic control, monitor mixing, and stage connection techniques"]
                    },
                    {
                        "phase_number": 4,
                        "title": "Studio Recording, Digital Audio & Branding",
                        "duration": "10 Months",
                        "objectives": ["Master Logic Pro or Ableton Live for tracking and audio editing", "Record, mix, and publish an original single on streaming platforms"]
                    }
                ]
            elif "software" in target_lower or "developer" in target_lower or "programmer" in target_lower or "full stack" in target_lower:
                timeline = "1.5 - 3 Years"
                score = 45.0
                phases = [
                    {
                        "phase_number": 1,
                        "title": "Programming Core & Computer Science Fundamentals",
                        "duration": "6 Months",
                        "objectives": ["Master a language (Python, Java, or JS) and Data Structures & Algorithms", "Learn Git version control, command line utilities, and testing"]
                    },
                    {
                        "phase_number": 2,
                        "title": "Web Architecture & Database Systems",
                        "duration": "12 Months",
                        "objectives": ["Build full-stack applications with React, Node.js, and Express", "Model relational databases (PostgreSQL/MySQL) and write complex queries"]
                    },
                    {
                        "phase_number": 3,
                        "title": "Distributed Cloud Systems & DevOps",
                        "duration": "12 Months",
                        "objectives": ["Deploy applications to AWS/GCP, configure Docker containers", "Set up CI/CD pipeline automations and explore microservices"]
                    }
                ]
            else:
                timeline = "1.5 - 2.0 Years"
                score = 40.0
                phases = [
                    {
                        "phase_number": 1,
                        "title": f"Foundational Skill Acquisition in {target_destination}",
                        "duration": "6 Months",
                        "objectives": [f"Learn core vocabulary and literature of {target_destination}", "Complete certification training courses in basic competencies"]
                    },
                    {
                        "phase_number": 2,
                        "title": f"Practical Application & Portfolio Creation",
                        "duration": "12 Months",
                        "objectives": [f"Complete 2-3 standalone projects highlighting {target_destination} skills", "Collaborate on peer review exercises and write technical logs"]
                    },
                    {
                        "phase_number": 3,
                        "title": f"Professional Strategy & Transition Plan",
                        "duration": "6 Months",
                        "objectives": [f"Tailor resume for junior {target_destination} job listings", "Attend industry conferences and build active professional networks"]
                    }
                ]
                
            raw_analysis = (
                f"### Personalized Career Pathfinder Roadmap (Offline Mode)\n\n"
                f"Bridging the transition from your current role to your target destination of **{target_destination}** "
                f"requires a structured learning path. We estimated a timeline of **{timeline}** based on your target skills."
            )
            
            return {
                "success": True,
                "is_mock": True,
                "raw_analysis": raw_analysis,
                "roadmap": {
                    "estimated_timeline": timeline,
                    "career_readiness_score": score,
                    "phases": phases
                }
            }

        # Return structured progression roadmap alongside raw text
        return {
            "success": True,
            "raw_analysis": result.detailed_analysis,
            "roadmap": {
                "estimated_timeline": result.estimated_timeline,
                "career_readiness_score": result.career_readiness_score,
                "phases": [m.model_dump() for m in result.phases]
            }
        }
