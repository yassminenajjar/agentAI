import pandas as pd
from app.services.gemini_service import GeminiService
from app.services.sql_service import SQLService
from app.services.visualisation_service import VisualizationService

class NLToSQLService:
    def __init__(self):
        self.gemini_service = GeminiService()
        self.sql_service = SQLService()
        self.visualization_service = VisualizationService()
    
    def is_relevant_query(self, user_query):
        """Check if the query is relevant to the database"""
        prompt = f"""
        You are a database query classifier. Your task is to determine if this user query:
        \"{user_query}\"

        is relevant to a database with this schema:
        {self.sql_service.schema_info}

        Respond with ONLY 'True' if the query is relevant and can be answered with this database,
        or 'False' if the query is completely unrelated to this database context.
        """
        response = self.gemini_service.generate_content(prompt)
        return response.strip().lower() == 'true'
    
    def generate_sql_query(self, user_query):
        """Convert natural language to SQL"""
        prompt = f"""
        Database Schema:
        {self.sql_service.schema_info}

        Convert this to SQL (ONLY the query, using SQL Server syntax):
        - Use YEAR() instead of strftime('%Y')
        - Use MONTH() instead of strftime('%m')
        - Use DAY() instead of strftime('%d')
        - Use CONVERT() for date formatting
        - If you use ORDER BY, always include the ordered column(s) in both the SELECT and GROUP BY clauses.

        User query: \"{user_query}\"
        """
        sql_response = self.gemini_service.generate_content(prompt)
        return self.gemini_service.clean_sql_response(sql_response)
    
    def generate_report(self, user_query, sql_query, results):
        """Generate a formatted report for analytical queries"""
        report_instruction = """Generate output EXACTLY in this format:

        [Report Title Brief Description]

        - [Item 1]: [Metric] ([Percentage if available])
        - [Item 2]: [Metric]
        - (...)

        Helpful Insights: [The top 3(if possible) remarks made from the result of SQL query execution,The remarks provided need to be helpful to a Business Intelligence perspective].

        Suggested Actions: [The top 3(if possible) actions that needs to be done about the remarks made in the Helpful Insights section even if the insights are not enough for you to suggest actions , suggest the ones you would if you were running a multi million dollar company that produces cables for car manufacturing and other industries  ].

        RULES:
        1. Title must be <10 words
        2. List all the items returned in the results of the SQL execution result 
        3. Helpful Insights must include a percentage or multiplier
        4. Suggested Actions must specify both what and where
        5. Never show SQL or technical details
        6. Use same punctuation/capitalization as example"""

        explanation_prompt = f"""
        Database Context:
        {self.sql_service.schema_info}

        User Question: {user_query}
        SQL Used: {sql_query}
        Query Results: {str(results)}

        {report_instruction}

        STRICT FORMATTING:
        - Blank line after title
        - Dash-start for list items
        - "Helpful Insights:" and "Suggested Actions:" labels exactly as shown
        """
        
        return self.gemini_service.generate_content(explanation_prompt)
    
    def generate_direct_answer(self, user_query, sql_query, results):
        """Generate a direct answer for simple queries"""
        explanation_prompt = f"""
        Database Context:
        {self.sql_service.schema_info}

        User Question: {user_query}
        SQL Used: {sql_query}
        Query Results: {str(results)}

        Answer in 1 line with the key number.

        STRICT FORMATTING:
        - No report structure, just answer the question directly.
        - Do NOT provide Helpful Insights or Suggested Actions.
        """
        
        return self.gemini_service.generate_content(explanation_prompt)
    
    def process_query(self, user_query):
        """Process a natural language query end-to-end"""
        if not self.is_relevant_query(user_query):
            return {
                "error": "The query is not relevant to this database context",
                "query": "",
                "results": None,
                "explanation": None,
                "visualization": None
            }
        
        sql_query = self.generate_sql_query(user_query)
        results = self.sql_service.execute_query(sql_query)
        
        is_report = any(keyword in user_query.lower() for keyword in 
                       ["analyze", "report", "trend", "compare", "summary", "breakdown"])
        
        if is_report:
            explanation = self.generate_report(user_query, sql_query, results)
        else:
            explanation = self.generate_direct_answer(user_query, sql_query, results)
        
        if isinstance(results, str) and results.startswith("Error"):
            plotly_code = None
            visualization = None
        else:
            plotly_code = self.visualization_service.generate_plotly_code(
                results, user_query, self.gemini_service.model
            )
            visualization = self.visualization_service.execute_plotly_code(
                plotly_code, results, user_query
            )
        
        return {
            "query": sql_query,
            "results": results.to_dict(orient='records') if isinstance(results, pd.DataFrame) else results,
            "explanation": explanation,
            "visualization": bool(visualization),  # Convert to boolean for JSON
            "plotly_code": plotly_code
        }