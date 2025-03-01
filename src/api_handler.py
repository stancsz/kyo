from flask import Flask, request, jsonify

app = Flask(__name__)

def update_file(file_name: str, file_content: str) -> None:
    # Update a file with new content
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(file_content)

def update_backlog(task: str, backlog: list) -> list:
    # Append a task to the backlog list and return the updated list
    backlog.append(task)
    return backlog

def process_api_request(payload: dict) -> dict:
    """
    Processes the API request payload.
    The payload should include an "operation" key with a value of either:
      - "update_file" (requires "file_name" and "file_content")
      - "update_backlog" (requires "task" and optional "backlog" list)
      
    If the operation is not recognized, returns an error message.
    """
    operation = payload.get("operation")
    if operation == "update_file":
        try:
            file_name = payload["file_name"]
            file_content = payload["file_content"]
            update_file(file_name, file_content)
            return {"status": "success", "message": f"File '{file_name}' updated successfully."}
        except KeyError:
            return {"status": "error", "message": "Missing file_name or file_content for update_file operation."}
    elif operation == "update_backlog":
        try:
            task = payload["task"]
            backlog = payload.get("backlog", [])
            updated_backlog = update_backlog(task, backlog)
            return {"status": "success", "updated_backlog": updated_backlog}
        except KeyError:
            return {"status": "error", "message": "Missing task for update_backlog operation."}
    else:
        return {"status": "error", "message": "Invalid or missing operation."}

@app.route("/api", methods=["POST"])
def api_handler():
    payload = request.get_json()
    response = process_api_request(payload)
    return jsonify(response)

if __name__ == "__main__":
    print("Starting API Handler. Use /api endpoint via POST requests.")
    app.run(debug=True)
