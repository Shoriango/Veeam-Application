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
        print(root)
        for dir_name in dirs:
            print(dir_name)
            dir_path = os.path.join(root, dir_name)
            replica_dir_path = os.path.join(replica_path, os.path.relpath(dir_path, source_path))

            if not os.path.exists(replica_dir_path):
                log_message(f"Creating directory '{replica_dir_path}'.", log_file)
                os.makedirs(replica_dir_path)

        for file_name in files:
            print(file_name)
            file_path = os.path.join(root, file_name)
            replica_file_path = os.path.join(replica_path, os.path.relpath(file_path, source_path))

            if not os.path.exists(replica_file_path):
                log_message(f"Copying file '{file_path}' to '{replica_file_path}'.", log_file)
                shutil.copy2(file_path, replica_file_path)



