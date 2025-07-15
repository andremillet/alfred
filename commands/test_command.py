class TestCommand:
    def __init__(self, agent):
        self.agent = agent

    def execute(self, args):
        if len(args) != 1:
            print("Usage: /test <test_file_path>")
            return

        test_file_path = args[0]
        
        try:
            test_tool = self.agent.tools['test_execution']
            result = test_tool.run_tests(test_file_path)
            
            print(f"Test results for '{test_file_path}':")
            print(f"Status: {result['status']}")
            if result['stdout']:
                print("Stdout:")
                print(result['stdout'])
            if result['stderr']:
                print("Stderr:")
                print(result['stderr'])
            if result['message']:
                print(f"Message: {result['message']}")

        except Exception as e:
            print(f"Error during test execution: {e}")
