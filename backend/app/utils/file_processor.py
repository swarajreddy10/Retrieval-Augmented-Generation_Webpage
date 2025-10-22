import os
import tempfile
import asyncio
from typing import Dict, Any
from pathlib import Path
import aiofiles
from PyPDF2 import PdfReader
import docx
import logging

logger = logging.getLogger(__name__)

class FileProcessor:
    SUPPORTED_EXTENSIONS = {'.pdf', '.txt', '.docx'}
    
    @classmethod
    async def extract_text_from_file(cls, file_path: str) -> Dict[str, Any]:
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.pdf':
            return await cls._extract_from_pdf(file_path)
        elif file_ext == '.txt':
            return await cls._extract_from_txt(file_path)
        elif file_ext == '.docx':
            return await cls._extract_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
    
    @classmethod
    async def _extract_from_pdf(cls, file_path: str) -> Dict[str, Any]:
        def _read_pdf():
            text = ""
            with open(file_path, "rb") as file:
                reader = PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() or ""
            return text
        
        loop = asyncio.get_event_loop()
        text = await loop.run_in_executor(None, _read_pdf)
        
        return {"text": text.strip(), "metadata": {"file_type": "pdf"}}
    
    @classmethod
    async def _extract_from_txt(cls, file_path: str) -> Dict[str, Any]:
        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
                text = await file.read()
        except UnicodeDecodeError:
            async with aiofiles.open(file_path, 'r', encoding='latin-1') as file:
                text = await file.read()
        
        return {"text": text.strip(), "metadata": {"file_type": "txt"}}
    
    @classmethod
    async def _extract_from_docx(cls, file_path: str) -> Dict[str, Any]:
        def _read_docx():
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text += paragraph.text + "\n"
            return text
        
        loop = asyncio.get_event_loop()
        text = await loop.run_in_executor(None, _read_docx)
        
        return {"text": text.strip(), "metadata": {"file_type": "docx"}}
    
    @classmethod
    async def save_uploaded_file(cls, upload_file) -> str:
        file_ext = Path(upload_file.filename).suffix
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=file_ext)
        
        try:
            content = await upload_file.read()
            temp_file.write(content)
            temp_file.flush()
            return temp_file.name
        finally:
            temp_file.close()
    
    @classmethod
    def cleanup_temp_file(cls, file_path: str):
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
        except Exception as e:
            logger.warning(f"Failed to cleanup temp file {file_path}: {str(e)}")
    
    @classmethod
    def validate_file(cls, filename: str, content_type: str, file_size: int, max_size: int) -> None:
        file_ext = Path(filename).suffix.lower()
        if file_ext not in cls.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {file_ext}")
        
        if file_size > max_size:
            raise ValueError(f"File size exceeds maximum ({max_size} bytes)")