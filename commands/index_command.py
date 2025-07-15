class IndexCommand:
    def __init__(self, agent):
        self.agent = agent

    def execute(self, args):
        self.agent.index_project()
        print("\n--- Functions Indexed ---")
        if not self.agent.code_index:
            print("No functions found.")
        for func_name, data in self.agent.code_index.items():
            relative_path = os.path.relpath(data['file_path'], self.agent.project_root)
            print(f"- {func_name} (in {relative_path})")
        print("-----------------------\n")

