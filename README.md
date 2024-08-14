Test task to syncronize a folder from source to replica, logging all the actions from copying to removing files / directories.

There is no need to install any libraries since everything was made with python included ones.

To start the program in console, simply run: python folder_sync.py

A log file will be created under the name "folder_sync.log" after the first syncronizathion aswell as the replica folder in case it doesnt exist already.

If using an IDE, sometimes changes will not happen instantly, possibly taking some seconds to appear in the IDE.

Notes:
On the main function, calling the paths and the sync interval setting could have been done with sys.argv, but to make the program more readable and easily accessible to users, it was instead added the file already to the code.

In case the sys.argv was used, the following code would have to be executed to start the python script:

python folder_sync.py <source_path> <replica_path> <sync_interval> <log_file_path> 

substituting all the variables here with the correct values
