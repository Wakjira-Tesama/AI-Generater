import os
import subprocess
import random
from datetime import datetime, timedelta

# Configuration
COMMIT_MESSAGES = [
    "Refactor video processing logic",
    "Update UI components for better UX",
    "Fix indentation in app.py",
    "Optimize video generation speed",
    "Add error handling to video editor",
    "Update dependencies",
    "Clean up temporary files",
    "Improve text overlay positioning",
    "Fix bug in speed adjustment",
    "Enhance file selection dialog",
    "Update documentation",
    "Refactor variable names for clarity",
    "Add comments to complex functions",
    "Optimize memory usage during rendering",
    "Update styling for editor tab",
    "Fix edge case in trimming logic",
    "Add support for more video formats",
    "Update README with new features",
    "Minor code cleanup",
    "Fix typo in user instructions"
]

def git_commit(date_str, message):
    # Set environment variables for the commit date
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = f"{date_str} T12:00:00"
    env["GIT_COMMITTER_DATE"] = f"{date_str} T12:00:00"
    
    # modify a log file to ensure we have something to commit
    with open("activity_log.txt", "a") as f:
        f.write(f"Commit on {date_str}: {message}\n")
        
    # Stage the file
    subprocess.run(["git", "add", "activity_log.txt"], check=True)
    
    # Commit
    subprocess.run(["git", "commit", "-m", message], env=env, check=True)
    print(f"Committed: {message} on {date_str}")

def run_backfill():
    # Dates
    today = datetime(2026, 2, 4)
    yesterday = today - timedelta(days=1)
    
    # Yesterday: 14 commits
    print(f"--- Processing Yesterday: {yesterday.date()} (14 commits) ---")
    for i in range(14):
        msg = random.choice(COMMIT_MESSAGES)
        # Add a slight time variation if needed, but for now fixed time is fine or we can vary it
        # varies hour slightly to avoid exact same timestamp collision if using seconds, 
        # but git accepts same time. Let's just use the function.
        git_commit(yesterday.strftime("%Y-%m-%d"), msg)
        
    # Today: 12 commits
    print(f"--- Processing Today: {today.date()} (12 commits) ---")
    for i in range(12):
        msg = random.choice(COMMIT_MESSAGES)
        git_commit(today.strftime("%Y-%m-%d"), msg)

if __name__ == "__main__":
    run_backfill()
