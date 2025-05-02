def get_schema_info(cursor):
    cursor.execute("""
        SELECT t.name AS table_name, c.name AS column_name, ty.name AS type_name
        FROM sys.tables t
        JOIN sys.columns c ON t.object_id = c.object_id
        JOIN sys.types ty ON c.user_type_id = ty.user_type_id
        ORDER BY t.name, c.column_id
    """)
    schema = {}
    for table, column, dtype in cursor.fetchall():
        schema.setdefault(table, []).append(f"{column} ({dtype})")
    return "\n".join([f"{table}({', '.join(cols)})" for table, cols in schema.items()])