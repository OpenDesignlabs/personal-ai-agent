import json
import time
import datetime
import os
import threading
import logging

# Path for task storage
TASKS_FILE = os.path.join("Data", "Tasks.json")

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_tasks(tasks):
    os.makedirs("Data", exist_ok=True)
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task(task_text, execution_time):
    """
    task_text: What to do
    execution_time: datetime string or seconds from now
    """
    tasks = load_tasks()
    new_task = {
        "id": int(time.time()),
        "task": task_text,
        "time": execution_time,
        "status": "pending"
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return f"Reminder set: {task_text} at {execution_time}"

def check_and_run_tasks(execute_callback):
    """Loop to check for due tasks. Runs in a separate thread."""
    while True:
        tasks = load_tasks()
        now = datetime.datetime.now()
        updated = False
        
        for task in tasks:
            if task["status"] == "pending":
                try:
                    task_time = datetime.datetime.strptime(task["time"], "%Y-%m-%d %H:%M:%S")
                    if now >= task_time:
                        logging.info(f"Executing task: {task['task']}")
                        execute_callback(task["task"])
                        task["status"] = "completed"
                        updated = True
                except Exception as e:
                    logging.error(f"Error executing task {task['id']}: {e}")
                    task["status"] = "error"
                    updated = True
        
        if updated:
            save_tasks(tasks)
        
        time.sleep(30) # Check every 30 seconds

def start_scheduler(execute_callback):
    thread = threading.Thread(target=check_and_run_tasks, args=(execute_callback,), daemon=True)
    thread.start()
    return thread
