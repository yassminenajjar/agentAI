from flask import Blueprint, request, jsonify
from app.controller.query_controller import QueryController

query_blueprint = Blueprint('query', __name__)
query_controller = QueryController()

@query_blueprint.route('/process', methods=['POST'])
def handle_query():
    """
    Unified endpoint for natural language query processing
    Accepts POST with JSON: {"query": "your natural language question"}
    Returns JSON with:
    - SQL query
    - Query results
    - Explanation/analysis
    - Visualization data
    """
    data = request.get_json()
    user_query = data.get('query')
    
    if not user_query:
        return jsonify({"error": "No query provided"}), 400
    
    result = query_controller.process_query(user_query)
     # Convert DataFrame to JSON if results are a DataFrame
    if hasattr(result['results'], 'to_dict'):
        result['results'] = result['results'].to_dict(orient='records')

    # Visualization is a Plotly figure; you may want to return a static image or HTML
    # For now, just indicate if a figure was generated
    result['visualization'] = bool(result['visualization'])
    return jsonify(result)
    
   
    
   

@query_blueprint.route('/schema', methods=['GET'])
def get_schema():
    """
    Endpoint to retrieve database schema information
    """
    schema_info = query_controller.get_schema_info()
    
    if 'error' in schema_info:
        return jsonify(schema_info), 500
    
    return jsonify(schema_info)