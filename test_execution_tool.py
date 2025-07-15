import subprocess
import os

class TestExecutionTool:
    """
    A tool for executing unit tests.
    """

    def run_tests(self, test_file_path: str) -> dict:
        """
        Executes unit tests in a specified file using pytest.

        :param test_file_path: The absolute path to the test file.
        :return: A dictionary containing the test execution results.
        """
        if not os.path.exists(test_file_path):
            return {"status": "error", "message": f"Test file not found: {test_file_path}"}

        try:
            # Assuming pytest is installed and available in the environment
            result = subprocess.run(
                ["pytest", test_file_path],
                capture_output=True,
                text=True,
                check=True
            )
            return {
                "status": "success",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.CalledProcessError as e:
            return {
                "status": "failed",
                "stdout": e.stdout,
                "stderr": e.stderr,
                "returncode": e.returncode,
                "message": f"Tests failed with error: {e}"
            }
        except FileNotFoundError:
            return {"status": "error", "message": "pytest command not found. Please ensure pytest is installed and in your PATH."}
        except Exception as e:
            return {"status": "error", "message": f"An unexpected error occurred: {e}"}

def get_tool() -> TestExecutionTool:
    """Returns an instance of the TestExecutionTool."""
    return TestExecutionTool()
