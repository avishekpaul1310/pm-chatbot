import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GoogleSheetService:
    def __init__(self):
        # Load credentials
        credentials_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_FILE')
        self.sheet_id = os.getenv('GOOGLE_SHEET_ID')
        
        # Define the scopes
        scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        
        # Authenticate and create client
        creds = Credentials.from_service_account_file(credentials_path, scopes=scope)
        self.client = gspread.authorize(creds)
        
    def get_all_projects(self):
        """Get all project data from the sheet"""
        try:
            sheet = self.client.open_by_key(self.sheet_id).sheet1
            data = sheet.get_all_records()
            return data
        except Exception as e:
            print(f"Error fetching data from Google Sheet: {e}")
            return []
    
    def get_project_by_name(self, project_name):
        """Get a specific project by name"""
        projects = self.get_all_projects()
        for project in projects:
            if project.get('Project Name', '').lower() == project_name.lower():
                return project
        return None
    
    def search_projects(self, query):
        """Search projects based on query"""
        projects = self.get_all_projects()
        results = []
        
        query = query.lower()
        for project in projects:
            # Search in all fields
            for key, value in project.items():
                if isinstance(value, str) and query in value.lower():
                    results.append(project)
                    break
        
        return results