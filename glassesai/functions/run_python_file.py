import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid = os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs
        if not valid:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", file_path_abs]
        if args:
            command.extend(args)

        completed = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )

        parts = []
        if completed.returncode != 0:
            parts.append(f"Process exited with code {completed.returncode}")
        if not completed.stdout and not completed.stderr:
            parts.append("No output produced")
        else:
            if completed.stdout:
                parts.append("STDOUT:\n" + completed.stdout)
            if completed.stderr:
                parts.append("STDERR:\n" + completed.stderr)

        return "\n".join(parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file relative to the working directory, with optional string arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of string arguments to pass to the Python file.",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Single command-line argument as a string.",
                ),
            ),
        },
        required=["file_path"],
    ),
)
