import os
import shutil
import time
import ctypes
import subprocess
import sys

# Set terminal size and center it on screen
def setup_terminal():
    os.system('mode con: cols=100 lines=30')
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        width = 800
        height = 500
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)
        ctypes.windll.user32.MoveWindow(hwnd, x, y, width, height, True)

# Check if script has admin rights
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Re-run the script as admin if not already
def run_as_admin():
    if not is_admin():
        print("🛡️ Requesting administrator privileges...")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
        sys.exit()

# Ask confirmation using a message box
def ask_confirmation():
    response = ctypes.windll.user32.MessageBoxW(
        0,
        "⚠️ This will perform automated system cleaning.\n\nProceed?",
        "System Cleaner",
        1  # OK/Cancel
    )
    return response == 1

# Function to delete files and folders inside a given path
def clean_folder(path):
    if path and os.path.exists(path):
        print(f"📁 Cleaning: {path}")
        try:
            for filename in os.listdir(path):
                file_path = os.path.join(path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                        if not os.path.exists(file_path):
                            print(f"✅ Deleted: {file_path}")
                        else:
                            print(f"❌ Failed to delete: {file_path}")
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        if not os.path.exists(file_path):
                            print(f"✅ Deleted: {file_path}")
                        else:
                            print(f"❌ Failed to delete: {file_path}")
                except Exception:
                    pass
        except Exception as e:
            print(f"  ⚠️ Error accessing {path}: {e}")
    else:
        print(f"  ❌ Path does not exist or is invalid: {path}")

# Optional: clear event logs
def clear_event_logs():
    print("🧾 Clearing Windows Event Logs...")
    logs = subprocess.getoutput('wevtutil el').splitlines()
    for log in logs:
        log = log.strip()
        if log:
            print(f"  🗑️ Clearing: {log}")
            subprocess.call(['wevtutil', 'cl', log], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

# Run Disk Cleanup silently using setup flags
def run_disk_cleanup():
    print("🧼 Running Disk Cleanup (silent mode)...")
    subprocess.call("cleanmgr /sagerun:1", shell=True)

# Setup Disk Cleanup options
def setup_disk_cleanup_options():
    print("⚙️ Setting up Disk Cleanup options...")
    subprocess.call("cleanmgr /sageset:1", shell=True)

# Main Execution
def main():
    setup_terminal()
    run_as_admin()

    if not ask_confirmation():
        print("❌ Cleaning cancelled. Exiting...")
        time.sleep(1)
        sys.exit()

    folders_to_clean = [
        r'C:\Windows\Prefetch',
        r'C:\Windows\Temp',
        os.environ.get("TEMP"),
        os.environ.get("TMP")
    ]

    print("\n🧹 Starting cleanup process...\n")
    for path in folders_to_clean:
        clean_folder(path)
        time.sleep(1)

    # Uncomment to clear logs too
    # clear_event_logs()

    run_disk_cleanup()

    print("\n✅ System cleaning complete!")

    NEON_GREEN = '\033[38;2;57;255;20m'
    RESET_COLOR = '\033[0m'
    print(f"{NEON_GREEN}\n Automated Temp File Cleanup Developed By: Baron \n{RESET_COLOR}")

    input("🔚 Done Cleaning. Press Enter to close the terminal...")

if __name__ == "__main__":
    main()
