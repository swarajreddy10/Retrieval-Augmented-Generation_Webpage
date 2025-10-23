import os
import time
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SimpleRAG:
    """Simple ChatGPT-like RAG without vector complexity"""
    
    def __init__(self):
        self.user_documents = {}  # {session_id: {"content": "", "filename": "", "timestamp": float}}
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.max_sessions = 200  # Limit concurrent sessions
    
    def upload_document(self, content: str, filename: str, session_id: str):
        """Store document content for specific session"""
        # Clean old sessions if limit exceeded
        if len(self.user_documents) >= self.max_sessions:
            self._cleanup_old_sessions()
        
        self.user_documents[session_id] = {
            "content": content, 
            "filename": filename, 
            "timestamp": time.time()
        }
        logger.info(f"Stored document for {session_id}: {filename} ({len(content)} chars)")
    
    def _cleanup_old_sessions(self):
        """Remove oldest 50 sessions"""
        if len(self.user_documents) < 50:
            return
        
        # Sort by timestamp and remove oldest 50
        sorted_sessions = sorted(self.user_documents.items(), key=lambda x: x[1]['timestamp'])
        for session_id, _ in sorted_sessions[:50]:
            del self.user_documents[session_id]
        logger.info(f"Cleaned up 50 old sessions. Current sessions: {len(self.user_documents)}")
    
    def clear_documents(self, session_id: str):
        """Clear document content for specific session"""
        if session_id in self.user_documents:
            del self.user_documents[session_id]
        logger.info(f"Cleared documents for {session_id}")
    
    def has_documents(self, session_id: str) -> bool:
        """Check if documents are loaded for session"""
        return session_id in self.user_documents and bool(self.user_documents[session_id]["content"].strip())
    
    async def query(self, question: str, session_id: str) -> Dict[str, Any]:
        """Process query with simple approach"""
        start_time = time.time()
        
        try:
            if self.has_documents(session_id):
                doc_data = self.user_documents[session_id]
                prompt = f"""You are Echo AI. Answer the user's question.

Available document content:
{doc_data['content'][:15000]}

User question: {question}

Answer naturally."""
                sources = [{"filename": doc_data['filename'], "chunk_id": "doc_1", "content": "Document available", "confidence": 1.0}]
            else:
                prompt = f"""You are Echo AI, an intelligent assistant.

User question: {question}

Answer naturally."""
                sources = []
            
            answer = await self._generate_response(prompt)
            
            return {
                "answer": answer,
                "sources": sources,
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