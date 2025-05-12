import subprocess

def git_commit_completed_task(task_id, message):
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"✅ Completed {task_id}: {message}"], check=True)
        print(f"✅ Committed task {task_id}")
    except subprocess.CalledProcessError:
        print("⚠️ Git commit failed. Ensure git is initialized.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        git_commit_completed_task(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python git_commit_task.py <task_id> <description>")
