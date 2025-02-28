import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .services.gsheet_service import GoogleSheetService
from .services.llm_service import LLMService
from .services.query_classifier import QueryClassifier

def index(request):
    """Render the chat interface"""
    return render(request, 'chatbot/index.html')

@csrf_exempt  # For simplicity in the MVP, we'll exempt CSRF
def chat(request):
    """Process chat requests"""
    if request.method != 'POST':
        return JsonResponse({'message': 'Only POST requests are allowed'})
    
    try:
        data = json.loads(request.body)
        query = data.get('message', '')
        
        if not query:
            return JsonResponse({'message': 'Please ask a question.'})
        
        # Initialize services
        gsheet_service = GoogleSheetService()
        llm_service = LLMService()
        query_classifier = QueryClassifier()
        
        # Check if query is project-specific
        is_project_specific = query_classifier.is_project_specific(query)
        
        if is_project_specific:
            # Extract project name if mentioned
            project_name = query_classifier.extract_project_name(query)
            
            if project_name and project_name.lower() != 'none':
                # Get specific project data
                project_data = gsheet_service.get_project_by_name(project_name)
            else:
                # Search in all projects
                project_data = gsheet_service.get_all_projects()
            
            # Generate response with project context
            system_prompt = """
            You are a project management assistant.
            Use the provided project data to answer the user's question accurately.
            If the requested information is not in the data, say so.
            Be concise and professional.
            """
            
            response = llm_service.get_completion(query, system_prompt, project_data)
        else:
            # Handle general questions
            response = llm_service.get_completion(query)
        
        return JsonResponse({'message': response})
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'message': f"Sorry, I encountered an error: {str(e)}"})