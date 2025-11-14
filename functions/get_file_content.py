import os

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_dir):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    max_chars = 10000
    try:
        with open(target_dir, 'r') as file:
            file_content = file.read()
            if len(file_content) > max_chars:
                return f'{file_content[0:10000]} [...File "{file_path}" truncated at 10000 characters]'
        return file_content
    except Exception as e:
        return f'Error reading files: {e}'
