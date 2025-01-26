import os
from git import init_or_update_repo
from utils import print_code_from_directory

# Example usage
if __name__ == "__main__":
    repo_name = "example-repo"
    init_or_update_repo(repo_name)

    directory = os.path.join("kyos_work_folder",repo_name)  # Replace with your directory path
    try:
        print_code_from_directory(
            directory_path=directory,
            file_extensions=['.py', '.js'],  # Specify extensions as needed
            recursive=True  # Set to False to avoid traversing subdirectories
        )
    except ValueError as ve:
        print(ve)