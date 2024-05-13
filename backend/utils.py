import aiofiles
import urllib
import uuid
from md2pdf.core import md2pdf
import mistune
from docx import Document
from htmldocx import HtmlToDocx

async def write_to_file(filename: str, text: str) -> None:
    """Asynchronously write text to a file in UTF-8 encoding.

    Args:
        filename (str): The filename to write to.
        text (str): The text to write.
    """
    # Convert text to UTF-8, replacing any problematic characters
    text_utf8 = text.encode('utf-8', errors='replace').decode('utf-8')

    async with aiofiles.open(filename, "w", encoding='utf-8') as file:
        await file.write(text_utf8)

async def write_text_to_md(text: str, filename: str = "") -> str:
    """Writes text to a Markdown file and returns the file path.

    Args:
        text (str): Text to write to the Markdown file.

    Returns:
        str: The file path of the generated Markdown file.
    """
    file_path = f"outputs/{filename}.md"
    await write_to_file(file_path, text)
    return file_path

async def write_md_to_pdf(text: str, filename: str = "") -> str:
    """Converts Markdown text to a PDF file and returns the file path.

    Args:
        text (str): Markdown text to convert.

    Returns:
        str: The encoded file path of the generated PDF.
    """
    file_path = f"outputs/{filename}.pdf"

    try:
        md2pdf(file_path,
               md_content=text,
               #md_file_path=f"{file_path}.md",
               css_file_path="./frontend/pdf_styles.css",
               base_url=None)
        print(f"Report written to {file_path}.pdf")
    except Exception as e:
        print(f"Error in converting Markdown to PDF: {e}")
        return ""

    encoded_file_path = urllib.parse.quote(file_path)
    return encoded_file_path

async def write_md_to_word(text: str, filename: str = "") -> str:
    """Converts Markdown text to a DOCX file and returns the file path.

    Args:
        text (str): Markdown text to convert.

    Returns:
        str: The encoded file path of the generated DOCX.
    """
    file_path = f"outputs/{filename}.docx"

    try:
        # Convert report markdown to HTML
        html = mistune.html(text)
        # Create a document object
        doc = Document()
        # Convert the html generated from the report to document format
        HtmlToDocx().add_html_to_document(html, doc)

        # Saving the docx document to file_path
        doc.save(file_path)
        
        print(f"Report written to {file_path}")

        encoded_file_path = urllib.parse.quote(file_path)
        return encoded_file_path
    
    except Exception as e:
        print(f"Error in converting Markdown to DOCX: {e}")
        return ""
used_urls = set()  # Set to store used URLs

def is_url_used(url: str) -> bool:
    """Check if the URL has already been used.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if the URL has been used, False otherwise.
    """
    return url in used_urls

def mark_url_as_used(url: str) -> None:
    """Mark the URL as used.

    Args:
        url (str): The URL to mark as used.
    """
    used_urls.add(url)
import re

def extract_urls_from_response(response: str) -> List[str]:
    """Extract URLs from the AI's response.

    Args:
        response (str): The AI's response text.

    Returns:
        List[str]: A list of extracted URLs.
    """
    # Regex pattern to extract URLs
    url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
    urls = re.findall(url_pattern, response)
    return urls
