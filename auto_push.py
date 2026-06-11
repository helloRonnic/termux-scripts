# auto_push.py — Script #3
# What this does:
# → Checks if any files in your scripts folder have changed
# → If yes: adds them, commits with today's date, pushes to GitHub
# → Logs exactly what it did and when
# → Runs automatically at 8:30am after Scripts 1 and 2
# → Your GitHub repo stays permanently up to date with zero effort

import subprocess
import os
from datetime import datetime

# ─────────────────────────────────────────
# SETTINGS
# ─────────────────────────────────────────

# Your scripts folder — where all your files live
SCRIPTS_DIR = "/data/data/com.termux/files/home/scripts"

# Log file — records every push attempt
LOG_FILE = os.path.join(SCRIPTS_DIR, "push_log.txt")

# ─────────────────────────────────────────
# HELPER — Run a shell command
# Returns: (success, output_text)
# ─────────────────────────────────────────

def run_command(command, cwd=None):
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=cwd or SCRIPTS_DIR
        )
        output = result.stdout.strip() + result.stderr.strip()
        success = result.returncode == 0
        return success, output.strip()

    except Exception as e:
        return False, str(e)

# ─────────────────────────────────────────
# STEP 1 — CHECK FOR CHANGES
# Git tells us if anything is new or changed
# If nothing changed, no point pushing
# ─────────────────────────────────────────

def check_for_changes():
    # git status --porcelain gives a clean list of changed files
    # Empty output = nothing changed
    success, output = run_command("git status --porcelain")

    if not success:
        return False, "Could not check git status"

    if not output:
        return False, "No changes — nothing to push"

    # Count how many files changed
    changed_files = [line for line in output.split("\n") if line.strip()]
    return True, changed_files

# ─────────────────────────────────────────
# STEP 2 — ADD ALL CHANGED FILES
# Stages everything for commit
# ─────────────────────────────────────────

def git_add():
    success, output = run_command("git add .")
    return success, output

# ─────────────────────────────────────────
# STEP 3 — COMMIT WITH DATED MESSAGE
# Auto-generates a clear commit message
# using today's date and time
# ─────────────────────────────────────────

def git_commit():
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")

    # Commit message format: "Auto update — 2026-06-11 08:30"
    message = f"Auto update — {date_str} {time_str}"

    success, output = run_command(f'git commit -m "{message}"')
    return success, output, message

# ─────────────────────────────────────────
# STEP 4 — PUSH TO GITHUB
# ─────────────────────────────────────────

def git_push():
    success, output = run_command("git push")
    return success, output

# ─────────────────────────────────────────
# LOGGER — Saves every result to push_log.txt
# So you always know what happened
# ─────────────────────────────────────────

def write_log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

# ─────────────────────────────────────────
# MAIN — Runs all steps in order
# ─────────────────────────────────────────

def main():
    print("\n" + "=" * 55)
    print("  AUTO GITHUB PUSHER")
    print("  Checking for changes and pushing to GitHub...")
    print("=" * 55 + "\n")

    # Make sure we are in the right folder
    os.chdir(SCRIPTS_DIR)

    # ── Check if anything changed ──
    print("  🔍 Checking for changes...")
    has_changes, change_info = check_for_changes()

    if not has_changes:
        message = change_info  # "No changes — nothing to push"
        print(f"  ℹ️  {message}")
        write_log(message)
        print("\n" + "=" * 55)
        print("  ✅ Nothing to do — repo already up to date")
        print("=" * 55 + "\n")
        return

    # List the changed files
    print(f"  ✅ Found {len(change_info)} changed file(s):\n")
    for f in change_info:
        print(f"     {f}")

    # ── Git Add ──
    print("\n  📦 Staging files...")
    add_success, add_output = git_add()

    if not add_success:
        msg = f"FAILED — git add error: {add_output}"
        print(f"  ❌ {msg}")
        write_log(msg)
        return

    print("  ✅ Files staged successfully")

    # ── Git Commit ──
    print("\n  💾 Committing...")
    commit_success, commit_output, commit_message = git_commit()

    if not commit_success:
        # Sometimes this means nothing actually changed after staging
        # (e.g. files were added but identical to last commit)
        if "nothing to commit" in commit_output:
            msg = "Nothing new to commit — files unchanged since last push"
            print(f"  ℹ️  {msg}")
            write_log(msg)
            print("\n" + "=" * 55)
            print("  ✅ Repo already up to date")
            print("=" * 55 + "\n")
            return
        else:
            msg = f"FAILED — git commit error: {commit_output}"
            print(f"  ❌ {msg}")
            write_log(msg)
            return

    print(f"  ✅ Committed: \"{commit_message}\"")

    # ── Git Push ──
    print("\n  🚀 Pushing to GitHub...")
    push_success, push_output = git_push()

    if push_success:
        msg = f"SUCCESS — pushed {len(change_info)} file(s): {commit_message}"
        print(f"  ✅ Pushed successfully!")
        write_log(msg)

        print("\n" + "=" * 55)
        print(f"  ✅ DONE — GitHub repo updated")
        print(f"  📁 Files pushed: {len(change_info)}")
        print(f"  💬 Commit: {commit_message}")
        print(f"  🌐 Live at: github.com/helloRonnic/termux-scripts")
        print(f"  📋 Log saved to: push_log.txt")
        print("=" * 55 + "\n")

    else:
        # Push failed — usually means network issue or auth problem
        msg = f"FAILED — git push error: {push_output[:100]}"
        print(f"  ❌ Push failed: {push_output[:150]}")
        write_log(msg)

        print("\n  💡 Common fixes:")
        print("  → Check your internet connection")
        print("  → Run 'git push' manually to see full error\n")

if __name__ == "__main__":
    main()
