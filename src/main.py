import os
import requests
from git import init_or_update_repo
from utils import print_code_from_directory

def scan_repo(directory: str) -> str:
    repo_data = ""
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                repo_data += f"# {file_path}\n{content}\n\n"
            except Exception as e:
                repo_data += f"# {file_path}\n<Error reading file: {e}>\n\n"
    return repo_data

def call_api(payload: dict) -> dict:
    url = "http://localhost:5000/api"
    response = requests.post(url, json=payload)
    return response.json()

def update_local_file(file_path: str, new_content: str):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

def process_edits(repo_directory: str, edits: list):
    for edit in edits:
        file_path = edit.get("file")
        content = edit.get("content")
        if file_path and content is not None:
            update_local_file(file_path, content)
            print(f"Updated file: {file_path}")

def main():
    repo_name = "example-repo"
    init_or_update_repo(repo_name)
    repo_dir = os.path.join(os.getcwd(), "kyos_work_folder", repo_name)
    
    repo_data = scan_repo(repo_dir)
    
    payload = {
        "operation": "process_repo",
        "repo_data": repo_data
    }
    response = call_api(payload)
    
    edits = response.get("edits", [])
    process_edits(repo_dir, edits)
    
    backlog = response.get("backlog", [])
    while backlog:
        payload = {
            "operation": "process_backlog",
            "backlog": backlog
        }
        response = call_api(payload)
        edits = response.get("edits", [])
        process_edits(repo_dir, edits)
        backlog = response.get("backlog", [])
    
    print("Repository processing and updates complete.")

if __name__ == "__main__":
    main()