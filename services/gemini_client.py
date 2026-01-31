"""Simple Gemini API client wrapper."""
import os
import google.generativeai as genai
from typing import Optional


class GeminiClient:
    """Simple wrapper for Gemini 2.0 Flash API calls."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini client.
        
        Args:
            api_key: Optional API key. If not provided, reads from GEMINI_API_KEY env var.
        
        Raises:
            ValueError: If API key is not found.
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment or provided")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    def generate_text(self, prompt: str, temperature: float = 0.7, max_tokens: int = 2048) -> str:
        """
        Generate text from Gemini model.
        
        Args:
            prompt: The prompt to send to the model
            temperature: Temperature for generation (default: 0.7)
            max_tokens: Maximum output tokens (default: 2048)
        
        Returns:
            Generated text as string
        
        Raises:
            Exception: If API call fails
        """
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': temperature,
                    'max_output_tokens': max_tokens,
                }
            )
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")