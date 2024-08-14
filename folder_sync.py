import os
import shutil
import time
import sys


def log_message(message, log_file):
    log_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_entry = f"{log_time} - {message}\n"

    with open(log_file, "a") as f:
        f.write(log_entry)


def sync_folders(source_path, replica_path, log_file):
    if not os.path.exists(source_path):
        log_message(f"Source path '{source_path}' does not exist. Exiting.", log_file)
        sys.exit(1)

    if not os.path.exists(replica_path):
        log_message(f"Replica path '{replica_path}' does not exist. Creating.", log_file)
        os.makedirs(replica_path)

    for root, dirs, files in os.walk(source_path):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            replica_dir_path = os.path.join(replica_path, os.path.relpath(dir_path, source_path))

            if not os.path.exists(replica_dir_path):
                log_message(f"Copying directory '{dir_path}' to '{replica_dir_path}'.", log_file)
                shutil.copytree(dir_path, replica_dir_path)

            if not os.path.exists(replica_dir_path):
                log_message(f"Creating directory '{replica_dir_path}'.", log_file)
                os.makedirs(replica_dir_path)

        for file_name in files:
            print(files)
            file_path = os.path.join(root, file_name)
            replica_file_path = os.path.join(replica_path, os.path.relpath(file_path, source_path))
            print(replica_file_path)

            if not os.path.exists(replica_file_path):
                log_message(f"Copying file '{file_path}' to '{replica_file_path}'.", log_file)
                shutil.copy2(file_path, replica_file_path)

            elif os.path.getmtime(file_path) > os.path.getmtime(replica_file_path):
                log_message(f"Updating file '{replica_file_path}'.", log_file)
                shutil.copy2(file_path, replica_file_path)

    log_message(f"Sync complete. {len(os.listdir(source_path))} files and directories copied to '{replica_path}'.",
                log_file)


def main():
    # This step could have been done with sys.argv, but I preferred to keep it simple and more readable.
    # with the sys.argv, the command to start the code would have been:
    # python folder_sync.py <source_path> <replica_path> <sync_interval> <log_file_path>

    source_path = "./source"
    replica_path = "./replica"
    sync_interval = 45
    log_file_path = "./folder_sync.log"

    sync_folders(source_path, replica_path, log_file_path)

    while True:
        sync_folders(source_path, replica_path, log_file_path)
        log_message(f"Synchronization complete. Waiting {sync_interval} seconds for next sync.", log_file_path)
        time.sleep(sync_interval)


if __name__ == '__main__':
    main()
