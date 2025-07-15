import os
import importlib.util
import readline
from code_parser import find_functions_in_file
from benchmarking_tool import get_tool as get_benchmarking_tool
from code_suggestion import get_tool as get_suggestion_tool
from test_execution_tool import get_tool as get_test_execution_tool

class AlfredAgent:
    """The main agent for Alfred. It understands the context and uses tools to act."""

    def __init__(self, project_root):
        self.project_root = project_root
        self.code_index = {}
        self.tools = {
            "code_parser": find_functions_in_file,
            "benchmarking": get_benchmarking_tool(),
            "suggestion": get_suggestion_tool(),
            "test_execution": get_test_execution_tool()
        }
        self.commands = {} # Store command instances
        self._load_commands() # Load commands dynamically
        self.index_project()


    def _load_commands(self):
        commands_dir = os.path.join(self.project_root, "commands")
        for filename in os.listdir(commands_dir):
            if filename.endswith("_command.py"):
                module_name = filename[:-3] # Remove .py
                command_name = "/" + module_name.replace("_command", "")
                
                spec = importlib.util.spec_from_file_location(module_name, os.path.join(commands_dir, filename))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Assuming the class name is CamelCase of the module name
                class_name = "".join(word.capitalize() for word in module_name.split("_"))
                command_class = getattr(module, class_name)
                self.commands[command_name] = command_class(self)
        print(f"Loaded commands: {list(self.commands.keys())}")


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

    def run_command(self, command_line):
        """Parses and executes a command."""
        parts = command_line.strip().split(maxsplit=1)
        command_name = parts[0]
        args = parts[1].split() if len(parts) > 1 else []

        if command_name == "/exit":
            print("Exiting Alfred.")
            return False # Signal to exit the main loop
        
        if command_name in self.commands:
            self.commands[command_name].execute(args)
        else:
            print(f"Unknown command: {command_name}")
        return True # Signal to continue the main loop

class Completer:
    def __init__(self, agent):
        self.agent = agent

    def __call__(self, text, state):
        line = readline.get_line_buffer()
        parts = line.lstrip().split()

        if len(parts) == 0 or (len(parts) == 1 and not line.endswith(' ')):
            options = [cmd + ' ' for cmd in self.agent.commands.keys() if cmd.startswith(text)]
            if '/exit'.startswith(text):
                options.append('/exit ')
        elif len(parts) > 1 or (len(parts) == 1 and line.endswith(' ')):
            command = parts[0]
            if command in ['/benchmark', '/suggest']: # These commands expect a function name
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
            command_line = input("> ")
            if not agent.run_command(command_line):
                break
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
