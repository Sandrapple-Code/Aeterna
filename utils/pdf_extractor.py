from loguru import logger
try:
    import pypdf
except ImportError:
    pypdf = None

def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extracts text from an uploaded Streamlit file (BytesIO / UploadedFile) using pypdf.
    If pypdf is not installed, falls back to a clean plain-text/binary parser to avoid crashes.
    """
    if not uploaded_file:
        return ""
        
    if pypdf is None:
        logger.warning("pypdf library not found in the running environment. Falling back to byte decodable extraction.")
        try:
            # Check if we can read bytes directly
            content = uploaded_file.read()
            uploaded_file.seek(0)
            text_data = content.decode("utf-8", errors="ignore")
            # Filter printable characters
            clean_text = "".join(ch for ch in text_data if ch.isprintable() or ch in "\n\r\t ")
            words = [w for w in clean_text.split() if len(w) > 2]
            if len(words) > 20:
                logger.info("Successfully recovered text content from file bytes fallback.")
                return " ".join(words)
            return f"Uploaded Resume: {uploaded_file.name} (pypdf is missing, fallback parsing)"
        except Exception as fallback_err:
            logger.error(f"Fallback reading failed: {fallback_err}")
            return f"Uploaded Resume: {uploaded_file.name}"

    try:
        logger.info(f"Extracting text from PDF resume: {uploaded_file.name}")
        reader = pypdf.PdfReader(uploaded_file)
        text_parts = []
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
        extracted = "\n".join(text_parts).strip()
        logger.info(f"Successfully extracted {len(extracted)} characters from resume.")
        return extracted
    except Exception as e:
        logger.error(f"Failed to extract text from PDF: {e}")
        return f"Uploaded Resume: {uploaded_file.name} (Parsing failed: {str(e)})"
