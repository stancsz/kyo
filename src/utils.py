import os
from typing import List

def print_code_from_directory(
    directory_path: str,
    file_extensions: List[str] = None,
    recursive: bool = True
) -> None:
    """
    Traverses the specified directory, finds code files based on given extensions,
    and prints their contents with clear file path indications.

    Parameters:
        directory_path (str): The path to the directory to traverse.
        file_extensions (List[str], optional): List of file extensions to include.
            Defaults to ['.py', '.js', '.java', '.cpp', '.c', '.ts', '.rb', '.go'].
        recursive (bool, optional): Whether to traverse subdirectories.
            Defaults to True.

    Raises:
        ValueError: If the specified directory does not exist.
    """
    if not os.path.isdir(directory_path):
        raise ValueError(f"The directory '{directory_path}' does not exist.")

    # Default file extensions if none are provided
    if file_extensions is None:
        file_extensions = ['.py', '.js', '.java', '.cpp', '.c', '.ts', '.rb', '.go']

    # Normalize extensions to lowercase
    file_extensions = [ext.lower() for ext in file_extensions]

    # Choose the appropriate walker based on recursion preference
    if recursive:
        walker = os.walk(directory_path)
    else:
        # If not recursive, os.walk will only yield the top directory
        walker = [(directory_path, [], os.listdir(directory_path))]

    for root, dirs, files in walker:
        for file in files:
            _, ext = os.path.splitext(file)
            if ext.lower() in file_extensions:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code = f.read()
                    # Clear and AI-friendly formatting
                    print(f"\n=== FILE PATH: {file_path} ===\n")
                    print("```python")  # You can change the language tag based on file type
                    print(code)
                    print("```\n")
                except (UnicodeDecodeError, PermissionError) as e:
                    print(f"Could not read file '{file_path}': {e}")
