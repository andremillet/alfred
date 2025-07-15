import os
from code_parser import find_functions_in_file

class AlfredAgent:
    """The main agent for Alfred. It understands the context and uses tools to act."""

    def __init__(self, project_root):
        self.project_root = project_root
        self.code_index = {}
        self.tools = {
            "code_parser": find_functions_in_file
        }
        self.index_project()

    def index_project(self):
        """Uses the code_parser tool to index all .py files in the project."""
        print("Alfred is indexing the project...")
        for root, _, files in os.walk(self.project_root):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    functions = self.tools["code_parser"](file_path)
                    self.code_index.update(functions)
        print(f"Indexing complete. {len(self.code_index)} functions found.")

    def run_command(self, command):
        """Parses and executes a command."""
        if command.strip() == "/index":
            print("\n--- Functions Indexed ---")
            if not self.code_index:
                print("No functions found.")
            for func_name, data in self.code_index.items():
                relative_path = os.path.relpath(data['file_path'], self.project_root)
                print(f"- {func_name} (in {relative_path})")
            print("-----------------------\n")
        else:
            print(f"Unknown command: {command}")

def main():
    """The main loop for the Alfred CLI."""
    project_root = os.path.dirname(__file__)
    agent = AlfredAgent(project_root)

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