import json
from celery.result import AsyncResult


task_id = "89b77842-a386-4f6f-a008-10466c3578bf"

result = AsyncResult(task_id)

# Check if the task is ready (completed)
if result.ready():
    if result.successful():
        # Task completed successfully
        result_value = result.result  # Retrieve the task result
    else:
        # Task failed
        result_value = result.result  # Contains the error message or exception
else:
    result_value = None

json_file_path = "result.json"

result_data = {
    "status": "success" if result.successful() else "failure",
    "result": result_value,
}

with open(json_file_path, "w") as json_file:
    json.dump(result_data, json_file)

print(json.dumps(result_data, indent=4))

