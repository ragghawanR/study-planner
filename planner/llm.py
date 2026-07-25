"""
LLM module for OpenAI integration.
"""
import json
import os
from typing import Optional, Dict
from datetime import datetime
import openai

from planner.models import StudyPlan


class LLMClient:
    """Manages communication with OpenAI API."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """Initialize LLM client."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        openai.api_key = self.api_key
        self.model = model
        self.max_retries = 3
    
    def generate_study_plan(self, prompt: str) -> Optional[StudyPlan]:
        """
        Generate a study plan using the prompt.
        
        Args:
            prompt: The structured prompt for the LLM
            
        Returns:
            StudyPlan object or None if generation fails
        """
        try:
            response = self._call_openai_api(prompt)
            
            if not response:
                print("❌ Empty response from OpenAI API")
                return None
            
            # Parse and validate response
            study_plan = self._parse_response(response)
            return study_plan
        
        except Exception as e:
            print(f"❌ Error generating study plan: {e}")
            return None
    
    def _call_openai_api(self, prompt: str) -> Optional[str]:
        """
        Call the OpenAI API with retry logic.
        
        Args:
            prompt: The prompt to send to OpenAI
            
        Returns:
            The API response or None if all retries fail
        """
        for attempt in range(self.max_retries):
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful AI study coach. Always respond with valid JSON."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
                
                # Extract the response text
                content = response['choices'][0]['message']['content']
                return content
            
            except openai.error.RateLimitError:
                print(f"⚠️  Rate limit hit. Retrying in a moment... (Attempt {attempt + 1}/{self.max_retries})")
                if attempt < self.max_retries - 1:
                    import time
                    time.sleep(2 ** attempt)  # Exponential backoff
            
            except openai.error.APIError as e:
                print(f"⚠️  API error: {e} (Attempt {attempt + 1}/{self.max_retries})")
                if attempt < self.max_retries - 1:
                    import time
                    time.sleep(1)
            
            except Exception as e:
                print(f"❌ Unexpected error calling OpenAI API: {e}")
                return None
        
        return None
    
    def _parse_response(self, response: str) -> Optional[StudyPlan]:
        """
        Parse and validate the JSON response from OpenAI.
        
        Args:
            response: The raw response text from OpenAI
            
        Returns:
            StudyPlan object or None if parsing fails
        """
        try:
            # Try to extract JSON from the response
            response_data = self._extract_json(response)
            
            if not response_data:
                print("❌ Could not extract JSON from response")
                print(f"Response: {response[:200]}...")
                return None
            
            # Validate required fields
            required_fields = ["summary", "tasks", "revision", "motivation"]
            for field in required_fields:
                if field not in response_data:
                    print(f"⚠️  Missing required field: {field}")
                    response_data[field] = "N/A"
            
            # Create StudyPlan object
            study_plan = StudyPlan(
                summary=response_data.get("summary", ""),
                tasks=response_data.get("tasks", []),
                revision=response_data.get("revision", []),
                motivation=response_data.get("motivation", ""),
                estimated_time_hours=response_data.get("estimated_time_hours", 3)
            )
            
            return study_plan
        
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            return None
        except Exception as e:
            print(f"❌ Error parsing response: {e}")
            return None
    
    def _extract_json(self, text: str) -> Optional[Dict]:
        """
        Extract JSON from text that may contain other content.
        
        Args:
            text: The text potentially containing JSON
            
        Returns:
            Parsed JSON dict or None
        """
        # Try direct parsing first
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # Try to find JSON object in text
        start = text.find('{')
        if start == -1:
            return None
        
        # Find matching closing brace
        end = text.rfind('}')
        if end == -1:
            return None
        
        json_str = text[start:end+1]
        
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None
    
    def validate_api_key(self) -> bool:
        """
        Validate the OpenAI API key by making a simple request.
        
        Returns:
            True if valid, False otherwise
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": "Say 'OK' if you can see this."
                    }
                ],
                max_tokens=10
            )
            return bool(response['choices'])
        except Exception as e:
            print(f"❌ API key validation failed: {e}")
            return False
