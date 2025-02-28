from .llm_service import LLMService

class QueryClassifier:
    def __init__(self):
        self.llm_service = LLMService()
    
    def is_project_specific(self, query):
        """Determine if a query is project-specific or general"""
        system_prompt = """
        You are a query classifier for a project management system. 
        Analyze the given query and determine if it is asking about specific project details 
        such as project status, timelines, team members, etc.
        
        Return only 'PROJECT_SPECIFIC' or 'GENERAL' without any explanation.
        """
        
        result = self.llm_service.get_completion(query, system_prompt)
        return result.strip() == "PROJECT_SPECIFIC"
    
    def extract_project_name(self, query):
        """Extract project name from query if applicable"""
        system_prompt = """
        Extract the project name mentioned in the query.
        If no specific project is mentioned, return 'NONE'.
        Return only the project name or 'NONE' without any explanation.
        """
        
        result = self.llm_service.get_completion(query, system_prompt)
        return None if result.strip() == "NONE" else result.strip()