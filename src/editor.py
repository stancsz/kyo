import os

def is_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read(1024)
        return True
    except Exception:
        return False

def get_text_files(directory):
    for root, dirs, files in os.walk(directory):
        # Remove directories that start with "."
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for file in files:
            full_path = os.path.join(root, file)
            if is_text_file(full_path):
                yield full_path

def main():
    directory = input("Input a directory: ").strip()
    for file_path in get_text_files(directory):
        print(f"# FILE: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            content = f"<Error reading file: {e}>"
        print(content)
        print()  # blank line between files

if __name__ == "__main__":
    main()