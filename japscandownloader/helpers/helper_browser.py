import json


def process_browser_log_entry(entry):
    response = json.loads(entry["message"])["message"]
    return response
