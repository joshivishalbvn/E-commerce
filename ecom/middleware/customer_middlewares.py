# import time
# from rich.console import Console
# from rich.table import Table
# from rich.panel import Panel

# console = Console()

# class DebuggingMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Start the timer
#         start_time = time.time()

#         # Process the request and get the response
#         response = self.get_response(request)

#         # Calculate the duration
#         duration = time.time() - start_time

#         # Create a rich table for displaying the log details
#         table = Table(title="🕒 Duration Details", title_justify="center", style="bold green", border_style="blue")

#         # Add columns
#         table.add_column("Attribute", style="bold magenta", justify="center")
#         table.add_column("Value", style="cyan", justify="center")

#         # Populate the table with request details
#         table.add_row("Request Method", request.method)
#         table.add_row("Request Path", request.path)
#         table.add_row("User", getattr(request.user, 'email', 'Anonymous'))
#         table.add_row("Duration", f"{duration:.4f} seconds")
#         table.add_row("Response Status", str(response.status_code))
#         table.add_row("Query Params", str(request.GET.dict()) or "None")

#         console.print(Panel(table, title="📊 Request Debug Info", border_style="blue", padding=(1, 2)))

#         return response


import time
class DebuggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        print("================= >> Duration Details << =====================")
        print(f"{'*' * 10} {request.path} took {duration:.2f} seconds {'*' * 10}")
        print("==============================================================")
        print()
        return response

from django.middleware.gzip import GZipMiddleware

class CompressionMiddleware(GZipMiddleware):
    def __init__(self, get_response):
        super().__init__(get_response)



from django.db import connection
from django.contrib.auth.models import User


class DatabaseQueryLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Clear previous query logs
        connection.queries_log.clear()
        
        # Process the request and get the response
        response = self.get_response(request)


        # Log database queries with details
        query_count = len(connection.queries)
        total_time = sum(float(query['time']) for query in connection.queries)
        
        print("================== >> Execution Details << ===================")
        print(f"{'*' * 13} Executed {query_count} queries in {total_time:.2f} seconds {'*' * 13}")
        print("==============================================================")
        print()
        
        # for query in connection.queries:
        #     print('\033[91m'+'query: ' + '\033[92m', query["sql"])
            # self.log_query_details(query)

        return response
    
    # def log_query_details(self, query):
    #     sql = query['sql']
    #     time = query['time']
        
    #     # Extract table names from the SQL query (basic extraction)
    #     if "FROM" in sql:
    #         # Get the part of the query after "FROM"
    #         from_clause = sql.split("FROM")[1]
    #         # Split the clause to get the table names
    #         table_names = from_clause.split()[0:2]  # Consider up to two tables for simplicity
    #         print('\033[91m'+'Executed Query: ' + '\033[92m', f"{sql.strip()} | Time: {time} seconds | Tables: {', '.join(table_names)}")