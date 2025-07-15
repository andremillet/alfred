import importlib.util
import os

class BenchmarkCommand:
    def __init__(self, agent):
        self.agent = agent

    def execute(self, args):
        if len(args) != 1:
            print("Usage: /benchmark <function_name>")
            return

        func_name = args[0]
        if func_name not in self.agent.code_index:
            print(f"Function '{func_name}' not found in index.")
            return

        func_info = self.agent.code_index[func_name]
        file_path = func_info['file_path']
        
        try:
            spec = importlib.util.spec_from_file_location(func_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            func_to_benchmark = getattr(module, func_name)

            benchmarking_tool = self.agent.tools['benchmarking']
            execution_time = benchmarking_tool.run(func_to_benchmark)
            
            print(f"Benchmarking '{func_name}':")
            print(f"Execution time (1000 runs): {execution_time:.6f} seconds")

        except Exception as e:
            print(f"Error during benchmark: {e}")
