"""Simple Gemini API client wrapper."""
import os
import warnings
from typing import Optional

# Suppress deprecation warning for hackathon (package still works)
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=FutureWarning)
    import google.generativeai as genai


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
        # Use gemini-1.5-flash for better free tier quotas
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
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
        import time
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
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
                error_str = str(e)
                # Check if it's a quota/rate limit error
                if "429" in error_str or "quota" in error_str.lower() or "rate" in error_str.lower():
                    if attempt < max_retries - 1:
                        # Extract retry delay if provided
                        if "retry in" in error_str.lower():
                            try:
                                import re
                                delay_match = re.search(r'retry in ([\d.]+)s', error_str.lower())
                                if delay_match:
                                    retry_delay = float(delay_match.group(1)) + 1
                            except:
                                pass
                        print(f"⚠️  Rate limit hit. Retrying in {retry_delay}s... (attempt {attempt + 1}/{max_retries})")
                        time.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                        continue
                    else:
                        raise Exception("API quota exceeded. Please wait a few minutes or check your API key limits at https://ai.google.dev/gemini-api/docs/rate-limits")
                else:
                    raise Exception(f"Gemini API error: {error_str}")
        
        raise Exception("Failed to generate response after retries")