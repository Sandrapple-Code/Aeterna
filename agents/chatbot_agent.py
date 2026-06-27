from typing import Any, Dict
from loguru import logger
from agents.base_agent import BaseAgent

class ChatbotAgent(BaseAgent):
    """
    Agent for interactive career coaching and Q&A conversations.
    Uses context from the chat history and generates responses using the LLM.
    """
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        user_message = input_data.get("message", "")
        history = input_data.get("history", [])

        # Build prompt incorporating history
        prompt_parts = ["You are Aeterna's AI career coach. Answer the user's career questions, guide them, and help them navigate their career path.\n"]
        
        # Add conversation context
        for msg in history[-10:]:
            role = "User" if msg["role"] == "user" else "Assistant"
            prompt_parts.append(f"{role}: {msg['content']}")

        prompt_parts.append(f"User: {user_message}")
        prompt_parts.append("Assistant:")

        prompt = "\n".join(prompt_parts)
        
        # Enforce highly detailed, step-by-step explanatory response
        system_instruction = (
            "You are a professional, encouraging AI career coach assisting a user on their career operating system Aeterna. "
            "Always answer the user's questions in a highly detailed, guiding, and explaining manner. "
            "Break down your advice into logical steps, provide clear examples, and offer actionable follow-up instructions."
        )

        try:
            logger.info("ChatbotAgent: Generating response using Gemini...")
            response = self.llm.generate_text(prompt, system_instruction=system_instruction)
            
            # If the response indicates an API client placeholder or connection failure, use local coach logic
            if not response or response.startswith("Error") or "[MOCK RESPONSE]" in response or "Failed to generate" in response:
                user_msg_lower = user_message.lower()
                if "resume" in user_msg_lower or "cv" in user_msg_lower:
                    response = (
                        "📄 **Auditing & Optimizing Your Resume**\n\n"
                        "To stand out to recruiters and pass Applicant Tracking Systems (ATS), you need to format your resume using a metrics-driven structure. "
                        "Here is a step-by-step optimization strategy:\n\n"
                        "1. **Use the STAR/XYZ Formula**: Don't just list tasks. Frame achievements as: *'Accomplished [X], as measured by [Y], by doing [Z]'*.\n"
                        "   * *Weak*: 'Responsible for writing Python scripts.'\n"
                        "   * *Strong*: 'Developed 12 Python automation scripts that reduced manual data entry time by 30%.'\n"
                        "2. **Address Skill Gaps**: Review the target job description and integrate missing technical keywords (e.g. Docker, SQL, Kubernetes) in your skills section.\n"
                        "3. **Format Cleanly**: Use standard fonts (Arial, Calibri) and a single-column layout so ATS parsers can read it without errors.\n\n"
                        "👉 **Action Step**: Go to the **Resume Studio** page in the sidebar, upload your current resume, and Aeterna will calculate an alignment score and give you tailored bullet suggestions!"
                    )
                elif "robot" in user_msg_lower or "mechatronic" in user_msg_lower or "hardware" in user_msg_lower or "electronics" in user_msg_lower:
                    response = (
                        "🤖 **Robotics & Mechatronics Guidance**\n\n"
                        "Transitioning into Robotics and Mechatronics involves blending Mechanical, Electrical, and Software engineering. Here is your strategic learning path:\n\n"
                        "1. **Embedded Software**: Master C and C++ programming, which are the industry standards for microcontrollers (e.g. STM32, Arduino, ESP32, Raspberry Pi Pico).\n"
                        "2. **Robot Operating System (ROS/ROS2)**: This is crucial. Learn to create nodes, publish/subscribe to topics, and use tools like RViz and Gazebo for 3D physics simulation.\n"
                        "3. **Control Theory**: Study kinematics, dynamics, and classic control loops like PID controllers, state estimation (Kalman filters), and sensor integration (IMUs, LIDARs, encoders).\n"
                        "4. **Practical Projects**: Build a physical 2-axis or 3-axis robotic arm, or an autonomous maze-solving rover to prove you can bridge software and physical hardware.\n\n"
                        "👉 **Next Step**: Go to **Career Discovery**, enter 'Robotics and Mechatronics Engineer' as your target career, upload your resume, and CareerForge will calculate your path!"
                    )
                elif "python" in user_msg_lower or "coding" in user_msg_lower or "program" in user_msg_lower or "c++" in user_msg_lower or "learn" in user_msg_lower:
                    response = (
                        "💻 **Mastering Programming & Software Engineering**\n\n"
                        "Developing high-quality coding skills is highly cumulative. Here is how Aeterna recommends structuring your practice:\n\n"
                        "1. **Choose a Core Language**: Use Python for Data Science/Machine Learning, C++ for Systems/Robotics, or JavaScript/TypeScript for Web Applications.\n"
                        "2. **Data Structures & Algorithms**: Learn arrays, lists, trees, and search/sort algorithms. Practice 1-2 questions daily on LeetCode or HackerRank to build problem-solving speed.\n"
                        "3. **Version Control (Git)**: Push all your project code to GitHub. Make clean commits, write clear README.md files, and practice branching.\n"
                        "4. **Clean Code**: Focus on modular architecture, writing docstrings, testing, and debugging rather than just making it work.\n\n"
                        "Let me know which language or framework you are trying to learn, and I can give you a curated syllabus!"
                    )
                elif "ml" in user_msg_lower or "machine learning" in user_msg_lower or "ai" in user_msg_lower or "data science" in user_msg_lower or "deep learning" in user_msg_lower:
                    response = (
                        "📊 **Machine Learning & Artificial Intelligence Roadmap**\n\n"
                        "To build production-grade AI solutions, focus on these core areas:\n\n"
                        "1. **Mathematics Foundation**: Probability, statistics, linear algebra (matrices/vectors), and calculus (derivatives for gradient descent).\n"
                        "2. **Core ML Libraries**: Master Python data libraries (NumPy, Pandas, Matplotlib) and classical ML models with Scikit-Learn.\n"
                        "3. **Deep Learning Frameworks**: Choose PyTorch or TensorFlow/Keras to build and train artificial neural networks for computer vision or NLP.\n"
                        "4. **Model Deployment (MLOps)**: Learn how to host models using Flask/FastAPI, containerize them with Docker, and track experiments using MLflow.\n\n"
                        "Let me know if you are interested in NLP, Computer Vision, or Recommendation Systems!"
                    )
                elif "interview" in user_msg_lower or "prepare" in user_msg_lower or "prep" in user_msg_lower:
                    response = (
                        "🤝 **Interview Preparation Strategy**\n\n"
                        "Succeeding in technical and behavioral interviews requires structured practice:\n\n"
                        "1. **System Design**: Study how to build scalable systems (load balancers, caching, CDN, databases replication). Learn to sketch architecture flowcharts.\n"
                        "2. **Coding Round**: Practice writing bug-free code on a whiteboard or compiler while speaking your thoughts out loud (talk through your time/space complexity).\n"
                        "3. **Behavioral Questions**: Prepare 4-5 stories from past projects or teams using the STAR method (Situation, Task, Action, Result) to demonstrate conflict resolution, leadership, or problem solving.\n\n"
                        "What company or role are you preparing for? I can help you mock test it!"
                    )
                elif "roadmap" in user_msg_lower or "phases" in user_msg_lower or "path" in user_msg_lower:
                    response = (
                        "🗺️ **Navigating Your Learning Roadmap**\n\n"
                        "Your personalized up-skilling path is divided into clear milestones to help you transition step-by-step from your current stage to your dream career destination. Here is how to navigate it:\n\n"
                        "* **Phase 1: Foundations & Core Upskilling**: Focus entirely on core concepts and programming fundamentals (e.g. Python syntax, data structures). Do not rush to build complex projects yet.\n"
                        "* **Phase 2: Portfolio Development**: Apply what you've learned by building 2-3 significant, standalone projects. Host them on GitHub with detailed README files.\n"
                        "* **Phase 3: Career Readiness**: Optimize your resume, prepare for technical interviews, and start applying to roles.\n\n"
                        "👉 **Action Step**: You can view your full interactive roadmap on the **Dashboard** and **Career Planner** tabs in the sidebar!"
                    )
                elif "opportunity" in user_msg_lower or "job" in user_msg_lower or "intern" in user_msg_lower or "hackathon" in user_msg_lower:
                    response = (
                        "💼 **Finding and Securing Opportunities**\n\n"
                        "Uncovering the right opportunities is crucial for building real-world experience. Here are the target channels Aeterna recommends focusing on:\n\n"
                        "1. **Internships & Fellowships**: Ideal for building early professional experience. Programs like the MLH Fellowship offer structured open-source project exposure.\n"
                        "2. **Hackathons**: Events on Devpost or MLH are high-leverage opportunities to build working prototypes in 48 hours, prove your skills, and network directly with sponsors.\n"
                        "3. **Target Companies**: Identify 5-10 companies that align with your career goals and monitor their careers page for junior or internship openings.\n\n"
                        "👉 **Action Step**: Check out the **Opportunities** tab in Aeterna to see active jobs, hackathons, and companies tailored for you. Click **'Click for more details'** next to any listing, and I will coach you on how to apply!"
                    )
                else:
                    response = (
                        f"👋 **Welcome! I am Aeterna's AI Career Coach.**\n\n"
                        f"I am here to guide your professional journey and help you build a solid path forward. "
                        f"To get the most out of Aeterna, here is how you can proceed:\n\n"
                        f"1. **Start with Discovery**: Go to the **Career Discovery** page and enter your education, skills, and goals. This feeds data into the CareerForge engine.\n"
                        f"2. **Audit Your Skills**: Upload your resume in **Resume Studio** to run a comparative analysis and get an alignment score.\n"
                        f"3. **Execute the Roadmap**: Track your learning milestones on the **Career Planner** and search active jobs in **Opportunities**.\n\n"
                        f"What specific goals or topics (like Robotics, Machine Learning, Coding, or Interview Prep) are you working towards today? Let me know, and I can give you custom tips!"
                    )

            return {
                "success": True,
                "response": response
            }
        except Exception as e:
            logger.error(f"ChatbotAgent: Error generating chat response: {e}")
            return {
                "success": True,
                "response": (
                    "👋 **Offline Coach Mode**\n\n"
                    "I am currently operating in offline mode. Let's make progress on your goals:\n\n"
                    "1. If you need resume feedback, let's look at missing skills. What certifications do you currently hold?\n"
                    "2. If you are preparing for interviews, I recommend practicing systems engineering questions and explaining your project architectures using simple diagrams.\n"
                    "Let me know what you want to focus on next!"
                )
            }
