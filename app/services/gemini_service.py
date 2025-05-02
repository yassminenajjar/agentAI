import google.generativeai as genai
from Config import config
from functools import lru_cache

class GeminiService:
    def __init__(self):
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(config.GEMINI_MODEL)
        self.last_call_time = 0
        self.min_delay = 1.0  # Add 1-second delay between calls
    @lru_cache(maxsize=100)
    def generate_content(self, prompt):
        """Generate content using Gemini model"""
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            raise RuntimeError(f"Gemini API error: {str(e)}")
    
    def clean_sql_response(self, sql_response):
        """Clean SQL response from markdown formatting"""
        return sql_response.replace('```sql', '').replace('```', '').strip()