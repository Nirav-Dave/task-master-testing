import json
import subprocess
import time

TASK_FILE = "tasklist.json"

def load_tasks():
    with open(TASK_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def run_tests():
    print("🧪 Running tests...")
    result = subprocess.run(["pytest"], capture_output=True, text=True)
    print(result.stdout)
    return result.returncode == 0

def execute_task(task):
    print(f"💡 Executing task: {task['description']}")
    # Simulate sending to Cursor AI (replace with actual call if needed)
    time.sleep(2)
    return

def get_task_by_id(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

def can_execute(task, completed_ids):
    if not task.get("depends_on"):
        return True
    return all(dep in completed_ids for dep in task["depends_on"])

def main():
    while True:
        tasks = load_tasks()
        completed_ids = [t["id"] for t in tasks if t["status"] == "done"]

        progress_made = False
        for task in tasks:
            if task["status"] != "pending":
                continue
            if not can_execute(task, completed_ids):
                continue

            execute_task(task)

            if task["type"] == "test_verify":
                if run_tests():
                    task["status"] = "done"
                else:
                    print("❌ Tests failed. Reverting related implementation to 'pending'...")
                    for t in tasks:
                        if task.get("depends_on") and t["id"] in task["depends_on"]:
                            t["status"] = "pending"
                    continue
            else:
                task["status"] = "done"

            save_tasks(tasks)
            progress_made = True
            break  # Only one task at a time

        if not progress_made:
            print("✅ All executable tasks are completed or blocked.")
            break

if __name__ == "__main__":
    main()
