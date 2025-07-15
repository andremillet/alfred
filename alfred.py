import os
import importlib.util
import readline
from code_parser import find_functions_in_file
from benchmarking_tool import get_tool as get_benchmarking_tool
from code_suggestion import get_tool as get_suggestion_tool

class AlfredAgent:
    """The main agent for Alfred. It understands the context and uses tools to act."""

    def __init__(self, project_root):
        self.project_root = project_root
        self.code_index = {}
        self.tools = {
            "code_parser": find_functions_in_file,
            "benchmarking": get_benchmarking_tool(),
            "suggestion": get_suggestion_tool()
        }
        self.commands = ["/index", "/benchmark", "/suggest", "/exit"]
        self.index_project()

    def index_project(self):
        """Uses the code_parser tool to index all .py files in the project."""
        print("Alfred is indexing the project...")
        self.code_index = {}
        for root, _, files in os.walk(self.project_root):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    functions = self.tools["code_parser"](file_path)
                    self.code_index.update(functions)
        print(f"Indexing complete. {len(self.code_index)} functions found.")

    def run_command(self, command):
        """Parses and executes a command."""
        parts = command.strip().split()
        command_name = parts[0]

        if command_name == "/index":
            self.index_project() # Re-index to show the list
            self._handle_index_command()
        elif command_name == "/benchmark":
            self._handle_benchmark_command(parts[1:])
        elif command_name == "/suggest":
            self._handle_suggest_command(parts[1:])
        else:
            print(f"Unknown command: {command_name}")

    def _handle_index_command(self):
        """Handles the /index command."""
        print("\n--- Functions Indexed ---")
        if not self.code_index:
            print("No functions found.")
        for func_name, data in self.code_index.items():
            relative_path = os.path.relpath(data['file_path'], self.project_root)
            print(f"- {func_name} (in {relative_path})")
        print("-----------------------\n")

    def _handle_benchmark_command(self, args):
        """Handles the /benchmark command."""
        if len(args) != 1:
            print("Usage: /benchmark <function_name>")
            return

        func_name = args[0]
        if func_name not in self.code_index:
            print(f"Function '{func_name}' not found in index.")
            return

        func_info = self.code_index[func_name]
        file_path = func_info['file_path']
        
        try:
            # Dynamically import the module
            spec = importlib.util.spec_from_file_location(func_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            func_to_benchmark = getattr(module, func_name)

            # Run the benchmark
            benchmarking_tool = self.tools['benchmarking']
            execution_time = benchmarking_tool.run(func_to_benchmark)
            
            print(f"Benchmarking '{func_name}':")
            print(f"Execution time (1000 runs): {execution_time:.6f} seconds")

        except Exception as e:
            print(f"Error during benchmark: {e}")

    def _handle_suggest_command(self, args):
        """Handles the /suggest command."""
        if len(args) != 1:
            print("Usage: /suggest <function_name>")
            return

        func_name = args[0]
        if func_name not in self.code_index:
            print(f"Function '{func_name}' not found in index.")
            return

        func_info = self.code_index[func_name]
        
        try:
            suggestion_tool = self.tools['suggestion']
            suggestion = suggestion_tool.get_suggestion(func_info['code'])
            
            print(f"Suggestion for '{func_name}':")
            print(suggestion)

        except Exception as e:
            print(f"Error during suggestion: {e}")

class Completer:
    def __init__(self, agent):
        self.agent = agent

    def __call__(self, text, state):
        line = readline.get_line_buffer()
        parts = line.lstrip().split()

        # Autocomplete for the command itself
        if len(parts) == 0 or (len(parts) == 1 and not line.endswith(' ')):
            options = [cmd + ' ' for cmd in self.agent.commands if cmd.startswith(text)]
        # Autocomplete for function names after a command
        elif len(parts) > 1 or (len(parts) == 1 and line.endswith(' ')):
            command = parts[0]
            if command in ['/benchmark', '/suggest']:
                prefix = parts[1] if len(parts) > 1 else ''
                options = [f for f in self.agent.code_index if f.startswith(prefix)]
            else:
                options = []
        else:
            options = []

        try:
            return options[state]
        except IndexError:
            return None

def main():
    """The main loop for the Alfred CLI."""
    project_root = os.path.dirname(__file__) or '.'
    agent = AlfredAgent(project_root)

    # Setup tab completion
    readline.set_completer(Completer(agent))
    readline.set_completer_delims(' ')
    readline.parse_and_bind("tab: complete")

    print("\nWelcome to AlfredOS. Type a command or '/exit' to quit.")

    while True:
        try:
            command = input("> ")
            if command.strip().lower() == "/exit":
                break
            agent.run_command(command)
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
