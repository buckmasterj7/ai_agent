import os

from google.genai import types

def write_file(working_directory, file_path, content):

    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not (target_file == abs_working_dir or target_file.startswith(abs_working_dir + os.sep)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, "w") as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name = "write_file",
    description = "Writes content to file in the specified file path, constrained to the working directory. Creates file if it doesn't exist.",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "The file path to write file content to, relative to the working directory."
            ),
            "content": types.Schema(
                type = types.Type.STRING,
                description = "Content to write to the file",
            ),

        },
        required = ["file_path", "content"],

    ),

)


