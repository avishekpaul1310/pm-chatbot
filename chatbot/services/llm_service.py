import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-4o-mini"
    
    def get_completion(self, prompt, system_prompt=None, project_data=None):
        """Get completion from OpenAI API"""
        messages = []
        
        # Add system prompt if provided
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        else:
            messages.append({
                "role": "system", 
                "content": "You are a helpful project management assistant. Answer questions concisely and accurately."
            })
        
        # Add project data context if available
        if project_data:
            context = "Here's the project data to help answer the query:\n"
            context += str(project_data)
            messages.append({"role": "system", "content": context})
        
        # Add user prompt
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return "I'm sorry, I couldn't process your request at the moment."