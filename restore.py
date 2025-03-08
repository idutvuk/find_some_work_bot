import shutil
import os
import glob

def restore_latest_backup():
    backup_dir = 'backup/'
    backup_pattern = os.path.join(backup_dir, 'variables_backup_*.json')
    backup_files = glob.glob(backup_pattern)
    
    if not backup_files:
        print("No backup files found.")
        return
    
    latest_backup = max(backup_files, key=os.path.getmtime)
    shutil.copy2(latest_backup, 'variables.json')
    print(f"Restored '{latest_backup}' to 'variables.json'.")

if __name__ == "__main__":
    restore_latest_backup()
