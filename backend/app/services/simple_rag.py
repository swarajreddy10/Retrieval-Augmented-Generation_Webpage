import os
import time
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SimpleRAG:
    """Simple ChatGPT-like RAG without vector complexity"""
    
    def __init__(self):
        self.document_content = ""
        self.document_filename = ""
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    def upload_document(self, content: str, filename: str):
        """Store document content as plain text"""
        self.document_content = content
        self.document_filename = filename
        logger.info(f"Stored document: {filename} ({len(content)} chars)")
    
    def clear_documents(self):
        """Clear all document content"""
        self.document_content = ""
        self.document_filename = ""
        logger.info("Cleared all documents")
    
    def has_documents(self) -> bool:
        """Check if documents are loaded"""
        return bool(self.document_content.strip())
    
    async def query(self, question: str) -> Dict[str, Any]:
        """Process query with simple approach"""
        start_time = time.time()
        
        try:
            if self.has_documents():
                prompt = f"""You are Echo AI. Answer the user's question.

Available document content:
{self.document_content[:15000]}

User question: {question}

Answer naturally."""
            else:
                prompt = f"""You are Echo AI, an intelligent assistant.

User question: {question}

Answer naturally."""
            
            answer = await self._generate_response(prompt)
            
            return {
                "answer": answer,
                "sources": [{"filename": self.document_filename, "chunk_id": "doc_1", "content": "Document available", "confidence": 1.0}] if self.has_documents() else [],
                "confidence": 0.9,
                "processing_time": time.time() - start_time
            }
            
        except Exception as e:
            logger.error(f"Query failed: {str(e)}")
            return {
                "answer": "I'm having trouble processing your question. Please try again.",
                "sources": [],
                "confidence": 0.0,
                "processing_time": time.time() - start_time
            }
    
    async def _generate_response(self, prompt: str) -> str:
        """Generate response using available LLM"""
        # Try Groq first
        if self.groq_api_key:
            try:
                from groq import Groq
                client = Groq(api_key=self.groq_api_key)
                
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=2000,
                    temperature=0.1
                )
                
                return completion.choices[0].message.content.strip()
            except Exception as e:
                logger.warning(f"Groq failed: {str(e)}")
        
        # Try Gemini as fallback
        if self.gemini_api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.gemini_api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=2000,
                        temperature=0.1,
                    )
                )
                
                return response.text.strip()
            except Exception as e:
                logger.warning(f"Gemini failed: {str(e)}")
        
        return "I'm having trouble connecting to AI services. Please check your API keys."