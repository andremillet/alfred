class SuggestCommand:
    def __init__(self, agent):
        self.agent = agent

    def execute(self, args):
        if len(args) != 1:
            print("Usage: /suggest <function_name>")
            return

        func_name = args[0]
        if func_name not in self.agent.code_index:
            print(f"Function '{func_name}' not found in index.")
            return

        func_info = self.agent.code_index[func_name]
        
        try:
            suggestion_tool = self.agent.tools['suggestion']
            suggestion = suggestion_tool.get_suggestion(func_info['code'])
            
            print(f"Suggestion for '{func_name}':")
            print(suggestion)

        except Exception as e:
            print(f"Error during suggestion: {e}")
