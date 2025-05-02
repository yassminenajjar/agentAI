from flask import jsonify
import logging
from app.services.nl_to_sql_service import NLToSQLService
from app.services.sql_service import SQLService

class QueryController:
    def __init__(self):
        self.nl_to_sql_service = NLToSQLService()
        self.sql_service = SQLService()
        self.logger = logging.getLogger('api')
    
    def process_query(self, user_query):
        """Process a natural language query and return complete response"""
        self.logger.info(f"Processing query: {user_query}")
        
        try:
            result = self.nl_to_sql_service.process_query(user_query)
            
            if 'error' in result:
                self.logger.warning(f"Query processing error: {result.get('error')}")
            else:
                self.logger.info(f"Successfully processed query: {user_query}")
            
            return result
        except Exception as e:
            self.logger.error(f"Error processing query '{user_query}': {str(e)}", exc_info=True)
            return {
                "error": "Internal server error",
                "message": str(e),
                "query": user_query
            }
    
    def get_schema_info(self):
        """Get database schema information"""
        try:
            return {
                "schema": self.sql_service.get_schema(),
                "status": "success"
            }
        except Exception as e:
            self.logger.error(f"Error fetching schema: {str(e)}", exc_info=True)
            return {
                "error": "Failed to fetch schema information",
                "status": "error"
            }