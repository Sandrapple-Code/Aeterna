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
        self.cell(0, 10, "Aeterna Career Operating System — Generated Report", border=0, align="L")
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
            pdf.set_font("helvetica", "B", 20)
            pdf.set_text_color(30, 41, 59)
            pdf.cell(0, 15, report_title, ln=True, align="C")
            pdf.ln(10)
            
            # Render Sections
            for sec in sections:
                title = sec.get("title", "Section")
                body = sec.get("body", "")
                
                pdf.set_font("helvetica", "B", 14)
                pdf.set_text_color(30, 41, 59)
                pdf.cell(0, 10, title, ln=True)
                pdf.ln(2)
                
                pdf.set_font("helvetica", "", 10)
                pdf.set_text_color(71, 85, 105)
                pdf.multi_cell(0, 6, body)
                pdf.ln(8)
                
            pdf.output(str(output_path))
            logger.info(f"Career Report PDF successfully saved to: {output_path}")
            return str(output_path.resolve())
            
        except Exception as e:
            logger.error(f"Failed to generate career report PDF: {e}")
            raise e

    def compile_full_report(self, analysis_result):
        """
        Compiles a full report from the pipeline analysis result
        """
        sections = []
        
        # Career Discovery section
        discovery = analysis_result.get("discovery", {})
        if discovery.get("success"):
            rec_career = discovery.get("career_matches", {}).get("recommended_career", "Unknown")
            sections.append({
                "title": "Recommended Career",
                "body": f"Your top recommended career path is: {rec_career}"
            })
        
        # Career Planner section
        planner = analysis_result.get("planner", {})
        roadmap = planner.get("roadmap", {})
        sections.append({
            "title": "Estimated Timeline",
            "body": roadmap.get("estimated_timeline", "12-18 Months")
        })
        
        # Generate filename
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"aeterna_career_report_{timestamp}.pdf"
        
        return self.generate_career_report_pdf("Aeterna Career Report", sections, filename)
