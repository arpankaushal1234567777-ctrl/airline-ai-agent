import pypdf


def extract_text_from_pdf(file_path: str, max_pages: int = 2, max_chars: int = 4000) -> str:
    """
    Extracts text from a PDF file with page and character limits to keep context small.
    """
    try:
        reader = pypdf.PdfReader(file_path)
        text_parts = []
        
        # Read only up to max_pages
        for i, page in enumerate(reader.pages):
            if i >= max_pages:
                break
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
                
        full_text = "\n".join(text_parts).strip()
        
        # Apply character limit
        if len(full_text) > max_chars:
            full_text = full_text[:max_chars] + "\n... [Content Truncated for Size]"
            
        return full_text
    except Exception as e:
        raise ValueError(f"Failed to parse PDF document: {e}")
