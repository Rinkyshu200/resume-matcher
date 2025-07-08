import fitz  # PyMuPDF
import streamlit as st
from typing import Optional
import io

def extract_text_from_file(uploaded_file) -> Optional[str]:
    """
    Extract text from uploaded file (PDF or TXT).
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        Extracted text as string or None if extraction fails
    """
    try:
        file_extension = uploaded_file.name.lower().split('.')[-1]
        
        if file_extension == 'pdf':
            return extract_text_from_pdf(uploaded_file)
        elif file_extension == 'txt':
            return extract_text_from_txt(uploaded_file)
        else:
            st.error(f"Unsupported file format: {file_extension}")
            return None
            
    except Exception as e:
        st.error(f"Error extracting text: {str(e)}")
        return None

def extract_text_from_pdf(uploaded_file) -> Optional[str]:
    """
    Extract text from PDF file using PyMuPDF.
    
    Args:
        uploaded_file: Streamlit uploaded file object containing PDF
        
    Returns:
        Extracted text as string or None if extraction fails
    """
    try:
        # Read the file bytes
        pdf_bytes = uploaded_file.read()
        
        # Open PDF document from bytes
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        text_content = ""
        
        # Extract text from each page
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text_content += page.get_text()
            
        pdf_document.close()
        
        # Clean up the text
        text_content = clean_extracted_text(text_content)
        
        return text_content if text_content.strip() else None
        
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
        return None

def extract_text_from_txt(uploaded_file) -> Optional[str]:
    """
    Extract text from TXT file.
    
    Args:
        uploaded_file: Streamlit uploaded file object containing text
        
    Returns:
        File content as string or None if extraction fails
    """
    try:
        # Read text file
        text_content = uploaded_file.read().decode('utf-8')
        
        # Clean up the text
        text_content = clean_extracted_text(text_content)
        
        return text_content if text_content.strip() else None
        
    except UnicodeDecodeError:
        try:
            # Try different encoding
            uploaded_file.seek(0)
            text_content = uploaded_file.read().decode('latin-1')
            text_content = clean_extracted_text(text_content)
            return text_content if text_content.strip() else None
        except Exception as e:
            st.error(f"Error decoding text file: {str(e)}")
            return None
    except Exception as e:
        st.error(f"Error extracting text from TXT: {str(e)}")
        return None

def clean_extracted_text(text: str) -> str:
    """
    Clean and normalize extracted text.
    
    Args:
        text: Raw extracted text
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Replace multiple whitespaces with single space
    import re
    text = re.sub(r'\s+', ' ', text)
    
    # Remove excessive line breaks
    text = re.sub(r'\n+', '\n', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text

def validate_file_size(uploaded_file, max_size_mb: int = 10) -> bool:
    """
    Validate uploaded file size.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        max_size_mb: Maximum allowed file size in MB
        
    Returns:
        True if file size is acceptable, False otherwise
    """
    if uploaded_file is None:
        return False
    
    file_size = uploaded_file.size
    max_size_bytes = max_size_mb * 1024 * 1024
    
    if file_size > max_size_bytes:
        st.error(f"File size ({file_size / 1024 / 1024:.1f} MB) exceeds maximum allowed size ({max_size_mb} MB)")
        return False
    
    return True

def get_file_info(uploaded_file) -> dict:
    """
    Get basic information about uploaded file.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        Dictionary containing file information
    """
    if uploaded_file is None:
        return {}
    
    return {
        'name': uploaded_file.name,
        'size': uploaded_file.size,
        'type': uploaded_file.type,
        'size_mb': round(uploaded_file.size / 1024 / 1024, 2)
    }
