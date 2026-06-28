import streamlit as st
from pathlib import Path
from utils.helpers import format_file_size
from services.pdf_service import PDFService


def render_reports_page() -> None:
    """
    Renders the Reports page
    """
    # Page header with home button
    col_home, col_title = st.columns([1, 5])
    with col_home:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_page = "Landing"
            st.rerun()
    with col_title:
        st.markdown('<div class="dashboard-title">📄 Reports</div>', unsafe_allow_html=True)
        st.markdown('<div class="dashboard-subtitle">Download your career reports</div>', unsafe_allow_html=True)
        
    # Generate report button
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    analysis_generated = st.session_state.get("analysis_generated")
    generate_btn = st.button("📄 Generate Report Now", type="primary", disabled=not analysis_generated, use_container_width=True)
    if not analysis_generated:
        st.caption("Complete a Career Analysis first.")
        
    if generate_btn and analysis_generated:
        with st.spinner("Generating your personalized career report..."):
            pdf_service = PDFService()
            pdf_path = pdf_service.compile_full_report(st.session_state.analysis_result, st.session_state.get("intake_data"))
            st.success("Report generated successfully!")
            st.rerun()
            
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.subheader("📂 Generated Reports")
    
    # List all PDF files in reports directory
    reports_dir = Path("reports")
    if not reports_dir.exists():
        st.info("No reports have been generated yet.")
        return
        
    pdf_files = list(reports_dir.glob("*.pdf"))
    if not pdf_files:
        st.info("No reports have been generated yet.")
        return
        
    # Sort files by modification time (newest first)
    pdf_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    for pdf_file in pdf_files:
        file_size = pdf_file.stat().st_size
        col_name, col_size, col_download, col_delete = st.columns([4, 1, 1, 1])
        
        with col_name:
            st.markdown(f"**{pdf_file.name}**")
        with col_size:
            st.text(format_file_size(file_size))
        with col_download:
            with open(pdf_file, "rb") as f:
                st.download_button(
                    "📥",
                    data=f,
                    file_name=pdf_file.name,
                    mime="application/pdf"
                )
        with col_delete:
            if st.button("🗑️", key=f"delete_{pdf_file.name}"):
                import os
                os.remove(pdf_file)
                st.success(f"Successfully deleted {pdf_file.name}")
                st.rerun()
