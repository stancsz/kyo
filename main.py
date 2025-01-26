import os
import subprocess
import base64

def init_or_update_repo(repo_name):
    """
    Checks if a GitHub repository exists, clones or pulls if it does,
    creates and pushes if it doesn't, inside the specified work folder.

    Args:
        repo_name (str): The name of the repository to create or update.
    """

    # Configuration details
    github_username = "kyoichi-dev"
    git_user_name = "kyoichitsu"
    encoded_email = "Ynl0ZW5yZWNvcmRzK2t5b2ljaGl0c3VAZ21haWwuY29t"  # Base64-encoded email
    git_user_email = base64.b64decode(encoded_email).decode()
    remote_url = f"git@github.com:{github_username}/{repo_name}.git"
    readme_content = f"# {repo_name}\n\nThis is an auto-generated repository."
    
    # Define work folder with lowercase and no spaces
    work_folder = os.path.join(os.getcwd(), "kyos_work_folder")
    os.makedirs(work_folder, exist_ok=True)  # Ensure the work folder exists

    repo_path = os.path.join(work_folder, repo_name)

    try:
        # Step 1: Check if the repository exists on GitHub
        repo_check_command = ["gh", "repo", "view", f"{github_username}/{repo_name}"]
        result = subprocess.run(repo_check_command, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"Repository '{repo_name}' already exists on GitHub.")

            # If the repo already exists, check if it's cloned locally
            if os.path.isdir(repo_path):
                print("Repository already cloned locally. Pulling the latest changes...")
                os.chdir(repo_path)
                subprocess.run(["git", "pull", "origin"], check=True)
            else:
                print("Cloning the repository...")
                subprocess.run(["git", "clone", remote_url, repo_path], check=True)
                os.chdir(repo_path)

        else:
            print(f"Repository '{repo_name}' does not exist. Creating it...")

            # Create the repository on GitHub
            subprocess.run(["gh", "repo", "create", f"{github_username}/{repo_name}", "--public"], check=True)

            # Create local repository directory
            os.makedirs(repo_path, exist_ok=True)
            os.chdir(repo_path)

            # Create README.md file
            with open("README.md", "w") as f:
                f.write(readme_content)

            # Git operations
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "config", "user.name", git_user_name], check=True)
            subprocess.run(["git", "config", "user.email", git_user_email], check=True)
            subprocess.run(["git", "add", "README.md"], check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)

            # Add remote and push
            subprocess.run(["git", "remote", "add", "origin", remote_url], check=True)
            subprocess.run(["git", "branch", "-M", "main"], check=True)
            subprocess.run(["git", "push", "-u", "origin", "main"], check=True)

            print(f"Repository '{repo_name}' created and pushed to GitHub successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        os.chdir(os.path.dirname(work_folder))  # Return to the original directory

# Example usage
if __name__ == "__main__":
    repo_name = "example-repo"
    init_or_update_repo(repo_name)
