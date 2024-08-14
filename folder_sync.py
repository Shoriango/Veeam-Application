import os
import shutil
import time
import sys


def log_message(message, log_file):
    """
    Format for log messages to insert into log file.
    """
    log_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_entry = f"{log_time} - {message}\n"

    with open(log_file, "a") as f:
        f.write(log_entry)

    print(log_entry)


def sync_folders(source_path, replica_path, log_file):
    """
    Main function use to synchronize source and replica folders.
    """
    # Check if source and replica paths exist
    if not os.path.exists(source_path):
        log_message(f"Source path '{source_path}' does not exist. Exiting.", log_file)
        sys.exit(1)

    if not os.path.exists(replica_path):
        # Create replica directory if it doesn't exist
        log_message(f"Replica path '{replica_path}' does not exist. Creating.", log_file)
        os.makedirs(replica_path)

    files_copied = []
    dirs_copied = []
    files_removed = []
    dirs_removed = []

    # Goes through all files of source
    for root, dirs, files in os.walk(source_path):
        # Checks if each directory in source exists in replica
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            replica_dir_path = os.path.join(replica_path, os.path.relpath(dir_path, source_path))

            if not os.path.exists(replica_dir_path):
                # in case it doesn't exist in replica, copy it
                log_message(f"Copying directory '{dir_name}'.", log_file)
                os.makedirs(replica_dir_path)
                dirs_copied.append(dir_name)

        # Checks if each file in source exists in replica
        for file_name in files:
            file_path = os.path.join(root, file_name)
            replica_file_path = os.path.join(replica_path, os.path.relpath(file_path, source_path))

            if not os.path.exists(replica_file_path):
                # in case it doesn't exist in replica, copy it
                log_message(f"Copying file '{file_name}'.", log_file)
                shutil.copy2(file_path, replica_file_path)
                files_copied.append(file_name)

            elif os.path.getmtime(file_path) > os.path.getmtime(replica_file_path):
                # in case there have been changes to the file (file has been updated in source), copy it
                log_message(f"Updating file '{file_name}' (changed in source).", log_file)
                shutil.copy2(file_path, replica_file_path)
                files_copied.append(file_name)

    # Goes through all files of replica and removes them if they don't exist in source
    for root, dirs, files in os.walk(replica_path, topdown=False):
        for file_name in files:
            replica_file_path = os.path.join(root, file_name)
            source_file_path = os.path.join(source_path, os.path.relpath(replica_file_path, replica_path))

            if not os.path.exists(source_file_path):
                # in case it doesn't exist in source, remove it
                log_message(f"Removing file '{file_name}' from replica directory.", log_file)
                os.remove(replica_file_path)
                files_removed.append(file_name)

        for dir_name in dirs:
            replica_dir_path = os.path.join(root, dir_name)
            source_dir_path = os.path.join(source_path, os.path.relpath(replica_dir_path, replica_path))

            if not os.path.exists(source_dir_path):
                # in case it doesn't exist in source, remove it
                log_message(f"Removing directory '{dir_name}' from replica directory.", log_file)
                shutil.rmtree(replica_dir_path)
                dirs_removed.append(dir_name)

    # Log results
    if files_copied or dirs_copied or files_removed or dirs_removed:
        # in case there were changes
        log_message(
            f"Sync complete. {len(files_copied)} files copied/updated, {len(dirs_copied)} "
            f"directories copied, {len(files_removed)} files removed, {len(dirs_removed)}"
            f" directories removed from '{replica_path}'.",
            log_file)

        if files_copied:
            log_message(f"Copied/Updated files: {', '.join(files_copied)}", log_file)

        if dirs_copied:
            log_message(f"Copied directories: {', '.join(dirs_copied)}", log_file)

        if files_removed:
            log_message(f"Removed files: {', '.join(files_removed)}", log_file)

        if dirs_removed:
            log_message(f"Removed directories: {', '.join(dirs_removed)}", log_file)
    else:
        # if there were no changes
        log_message("No changes were made during synchronization.", log_file)


def main():
    """
    Main function that starts synchronization.
    """
    # paths and setting for synchronization
    source_path = "./source"
    replica_path = "./replica"
    sync_interval = 30
    log_file_path = "./folder_sync.log"

    try:
        # start synchronization until user stops it
        while True:
            sync_folders(source_path, replica_path, log_file_path)
            log_message(f"Synchronization complete. Waiting {sync_interval} seconds for next sync.", log_file_path)
            # wait for next sync
            time.sleep(sync_interval)
    except KeyboardInterrupt:
        # in case user stops synchronization
        log_message("Synchronization stopped by user.", log_file_path)
        print("Synchronization stopped.")


if __name__ == '__main__':
    main()
