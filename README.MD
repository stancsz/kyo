# Kyoichi AI Agent

Kyoichi is an AI agent inspired by and named after my friend Kyoichi, an artist with a creative flair. This project is designed to assist with automating tasks, managing repositories, and enhancing productivity, much like Devin AI.

## Features

- **GitHub Repository Management**: Automatically checks, clones, creates, and updates repositories.
- **Directory Organization**: All repositories are neatly stored in a dedicated folder structure (`kyos_work_folder`).
- **Automated Git Configuration**: Simplifies Git operations by auto-configuring user details and performing commits.
- **Error Handling**: Gracefully handles errors during Git and GitHub operations.

## Getting Started

### Prerequisites

- Python 3.6+
- Git
- GitHub CLI (`gh`)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/<your-github-username>/kyoichi-ai-agent.git
   cd kyoichi-ai-agent
   ```

2. Install dependencies (if any).

3. Make sure `gh` is authenticated to your GitHub account:
   ```bash
   gh auth login
   ```

### Usage

Run the script to manage your GitHub repositories:
```bash
python3 script.py
```

### Example

To create or update a repository named `example-repo`:
```bash
python3 script.py
```

Kyoichi AI will ensure the repository exists on GitHub and is synchronized locally.