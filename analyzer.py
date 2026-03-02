import ast
import re

# Function to check if the given Python code has valid syntax
def check_syntax(code):
    try:
        ast.parse(code) # Parse the code into an AST
        return True # If parsing succeeds, syntax is correct
    except SyntaxError as e:
        return False # If parsing fails, syntax error exists
# Function to check if the code is too long (more than 50 lines)
def check_long_function(code):
    lines = code.split("\n") # Split code into lines
    if len(lines) > 50:
        return "Code is too long (more than 50 lines)"
    return None
# Function to check whether comments are present in the code
def check_comments(code):
    if "#" not in code: # Check for presence of comment symbol
        return "No comments in code"
    return None
# Function to detect single-character variable names (poor naming practice)
def check_variable_names(code):
    pattern = r"\b[a-zA-Z]{1}\b" # Regex to find single-letter variable names
    matches = re.findall(pattern, code)
    if matches:
        return "Single character variable names detected"
    return None
# Main function to analyze code and collect issues
def analyze_code(code):
    issues = []
    # Check syntax
    syntax_status = check_syntax(code)
    # Check if code is too long
    long_issue = check_long_function(code) 
    if long_issue:
        issues.append(long_issue)
     # Check for comments
    comment_issue = check_comments(code)  
    if comment_issue:
        issues.append(comment_issue)
     # Check variable naming
    variable_issue = check_variable_names(code)
    if variable_issue:
        issues.append(variable_issue)

    return syntax_status, issues
