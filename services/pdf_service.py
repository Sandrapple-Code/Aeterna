import os
from pathlib import Path
from fpdf import FPDF
from loguru import logger
from config.settings import get_settings

class AeternaPDF(FPDF):
    """
    Custom FPDF class to define professional layouts, headers, and footers.
    """
    def header(self) -> None:
        # Document title / header styling
        self.set_font("helvetica", "B", 8)
        self.set_text_color(100, 110, 120)
        self.cell(0, 10, "Aeterna Career Operating System - Generated Report", border=0, align="L")
        self.cell(0, 10, "Powered by CareerForge", border=0, align="R")
        self.ln(12)
        
        # Draw a subtle separator line
        self.set_draw_color(220, 225, 230)
        self.line(10, 20, 200, 20)

    def footer(self) -> None:
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        # Page number
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


class PDFService:
    """
    Service for compiling high-quality PDF resumes and career reports.
    """

    def __init__(self) -> None:
        self.settings = get_settings()
        self.output_dir = Path("reports")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info("PDFService initialized. Reports output directory: reports/")

    def generate_resume_pdf(self, candidate_name: str, content: str, filename: str = "optimized_resume.pdf") -> str:
        """
        Compiles a professional resume PDF from structured markdown/text.
        Returns the absolute path to the generated file.
        """
        logger.info(f"Generating resume PDF for candidate: {candidate_name}")
        
        # Safe output path
        output_path = self.output_dir / filename
        
        try:
            pdf = AeternaPDF(orientation="P", unit="mm", format="A4")
            pdf.alias_nb_pages()
            pdf.add_page()
            
            # Set Margins
            pdf.set_margins(15, 20, 15)
            
            # Render Candidate Name
            pdf.set_font("helvetica", "B", 24)
            pdf.set_text_color(30, 41, 59) # Slate 800
            pdf.cell(0, 15, candidate_name, ln=True, align="L")
            
            # Space
            pdf.ln(5)
            
            # Render Resume Body
            pdf.set_font("helvetica", "", 10)
            pdf.set_text_color(71, 85, 105) # Slate 600
            
            # Simple line-by-line wrapping
            for line in content.split("\n"):
                if not line.strip():
                    pdf.ln(3)
                    continue
                
                # Simple markdown bold detection
                if line.startswith("## "):
                    pdf.ln(4)
                    pdf.set_font("helvetica", "B", 14)
                    pdf.set_text_color(15, 23, 42) # Slate 900
                    pdf.cell(0, 10, line.replace("## ", ""), ln=True)
                    pdf.set_font("helvetica", "", 10)
                    pdf.set_text_color(71, 85, 105)
                elif line.startswith("- "):
                    pdf.multi_cell(0, 6, f"  {line}")
                else:
                    pdf.multi_cell(0, 6, line)
            
            pdf.output(str(output_path))
            logger.info(f"Resume PDF successfully saved to: {output_path}")
            return str(output_path.resolve())

        except Exception as e:
            logger.error(f"Failed to generate resume PDF: {e}")
            raise e

    def generate_career_report_pdf(self, report_title: str, sections: list[dict], filename: str = "career_report.pdf") -> str:
        """
        Generates a comprehensive multi-page Career Transition Report.
        """
        logger.info(f"Generating career transition report: {report_title}")
        output_path = self.output_dir / filename
        
        try:
            pdf = AeternaPDF(orientation="P", unit="mm", format="A4")
            pdf.alias_nb_pages()
            pdf.add_page()
            
            # Title Page/Header
            pdf.set_font("helvetica", "B", 18)
            pdf.set_text_color(30, 41, 59)
            sanitized_title = report_title.encode('latin-1', 'replace').decode('latin-1')
            pdf.cell(0, 15, sanitized_title, ln=True, align="C")
            pdf.ln(10)
            
            # Render Sections
            for sec in sections:
                title = sec.get("title", "Section")
                body = sec.get("body", "")
                
                pdf.set_font("helvetica", "B", 12)
                pdf.set_text_color(30, 41, 59)
                sanitized_sec_title = title.encode('latin-1', 'replace').decode('latin-1')
                pdf.cell(0, 10, sanitized_sec_title, ln=True)
                pdf.ln(2)
                
                pdf.set_font("helvetica", "", 10)
                pdf.set_text_color(71, 85, 105)
                # Sanitize to prevent UnicodeEncodeError (Latin-1 fallback)
                sanitized_body = body.encode('latin-1', 'replace').decode('latin-1')
                pdf.multi_cell(0, 6, sanitized_body)
                pdf.ln(6)
                
            pdf.output(str(output_path))
            logger.info(f"Career Report PDF successfully saved to: {output_path}")
            return str(output_path.resolve())
            
        except Exception as e:
            logger.error(f"Failed to generate career report PDF: {e}")
            raise e

    def compile_full_report(self, analysis_result, intake_data=None):
        """
        Compiles a full report from the pipeline analysis result.
        """
        sections = []
        
        # User details / Intake data
        name = "John Doe"
        if intake_data:
            name = intake_data.get("name", "John Doe")
            
        profile_body = f"Candidate Name: {name}\n"
        if intake_data:
            profile_body += (
                f"Education Level: {intake_data.get('education', 'N/A')}\n"
                f"Preferred Work Style: {intake_data.get('work_style', 'N/A')}\n"
                f"Career Goals: {intake_data.get('goals', 'N/A')}\n"
            )
        sections.append({
            "title": "1. Candidate Profile Summary",
            "body": profile_body
        })
        
        # Career Discovery section
        discovery = analysis_result.get("discovery", {})
        if discovery and discovery.get("success"):
            disc_matches = discovery.get("career_matches", {})
            rec_career = disc_matches.get("recommended_career", "Unknown")
            body_text = f"Top Recommended Career: {rec_career}\n\nTop Match:\n"
            matches = disc_matches.get("top_matches", [])
            if matches:
                match = matches[0]
                body_text += (
                    f"Match 1: {match.get('title', 'N/A')}\n"
                    f" - Fit Reason: {match.get('fit_reason', 'N/A')}\n"
                    f" - Industry Demand: {match.get('industry_demand', 'N/A')}\n"
                )
            sections.append({
                "title": "2. Career Alignment Summary (Concise)",
                "body": body_text
            })
            
        # Resume Studio section
        resume = analysis_result.get("resume")
        if resume and resume.get("success"):
            insights = resume.get("structured_insights", {})
            score = insights.get("match_score", 0)
            
            gaps_list = insights.get("skill_gaps_identified", [])[:2]
            gaps = "\n - ".join(gaps_list) if gaps_list else "No critical gaps identified."
            
            bullets_list = insights.get("optimized_bullets_suggested", [])[:1]
            bullets = "\n - ".join(bullets_list) if bullets_list else "No bullet suggestions needed."
            
            body_text = (
                f"Resume Match Score: {score}%\n\n"
                f"Top Skill Gaps:\n - {gaps}\n\n"
                f"Key Bullet Suggestion:\n - {bullets}"
            )
            sections.append({
                "title": "3. Resume Optimization Overview (Concise)",
                "body": body_text
            })
            
        # Career Planner section
        planner = analysis_result.get("planner", {})
        if planner and planner.get("success"):
            roadmap = planner.get("roadmap", {})
            timeline = roadmap.get("estimated_timeline", "12-18 Months")
            readiness = roadmap.get("career_readiness_score", 70)
            
            body_text = f"Estimated Timeline: {timeline}\nCareer Readiness Score: {readiness}%\n\nPrimary Phase:\n"
            phases = roadmap.get("phases", [])
            if phases:
                phase = phases[0]
                objs = "\n    * ".join(phase.get("objectives", [])[:2])
                body_text += (
                    f"Phase {phase.get('phase_number', 1)}: {phase.get('title', 'N/A')} ({phase.get('duration', 'N/A')})\n"
                    f"  Key Objectives:\n    * {objs}\n"
                )
            sections.append({
                "title": "4. Target Up-skilling Roadmap (Concise)",
                "body": body_text
            })
            
        # Opportunities section
        opp_res = analysis_result.get("opportunities", {})
        if opp_res and opp_res.get("success"):
            opps = opp_res.get("opportunities", {})
            body_text = ""
            for cat, items in [
                ("Jobs", opps.get("jobs", [])[:2]),
                ("Internships", opps.get("internships", [])[:2]),
                ("Hackathons", opps.get("hackathons", [])[:2]),
                ("Recommended Companies", opps.get("recommended_companies", [])[:2])
            ]:
                if items:
                    body_text += f"{cat}:\n"
                    for item in items:
                        if isinstance(item, str):
                            body_text += f" - {item}\n"
                        else:
                            body_text += f" - {item.get('title', 'N/A')}\n"
                    body_text += "\n"
            sections.append({
                "title": "5. Industry Opportunities Brief (Concise)",
                "body": body_text
            })
            
        # Motivational Quote and Message
        support_message = (
            "Motivational Quote:\n"
            "\"The only way to do great work is to love what you do.\" - Steve Jobs\n\n"
            "Supportive Message from Aeterna:\n"
            "Aeterna is proud to accompany you on your professional journey. Believe in your potential, "
            "leverage your custom learning roadmap, and continue the journey towards your desired path. "
            "Your future is built on the steps you take today!"
        )
        sections.append({
            "title": "6. Aeterna's Supportive Message & Motivational Quote",
            "body": support_message
        })
        
        # Generate filename
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"aeterna_career_report_{timestamp}.pdf"
        
        return self.compile_career_report(f"Aeterna Career Analysis Report - {name}", sections, filename)

    def compile_career_report(self, report_title: str, sections: list[dict], filename: str) -> str:
        """
        Internal wrapper to call generation method and match path.
        """
        return self.generate_career_report_pdf(report_title, sections, filename)
