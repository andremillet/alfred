
import ast
import os

def find_functions_in_file(file_path):
    """
    Analyzes a Python file and returns a dictionary of functions found.

    Args:
        file_path (str): The absolute path to the Python file.

    Returns:
        dict: A dictionary where keys are function names and values are
              dicts containing metadata like file_path, start_line, etc.
              Returns an empty dictionary if the file cannot be parsed.
    """
    if not os.path.exists(file_path):
        return {}

    with open(file_path, "r", encoding="utf-8") as source:
        try:
            tree = ast.parse(source.read(), filename=file_path)
        except SyntaxError:
            return {}

    functions = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions[node.name] = {
                "file_path": file_path,
                "start_line": node.lineno,
                "end_line": node.end_lineno,
                "parameters": [arg.arg for arg in node.args.args]
            }
    return functions
