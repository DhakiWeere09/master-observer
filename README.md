# master-observer
## File System Monitor with Real-Time Change Detection
This Python project recursively scans a file system, mapping files and their associated metadata (e.g., filename, last accessed date, size) into a structured format. It then runs an infinite loop, continuously monitoring the file system for changes in metadata. When any changes are detected, the user is notified through real-time alerts using the pyttsx3 offline text-to-speech library.
___

Features:
+ Recursive File Scanning: Automatically maps all files and metadata in the specified directory.
+ Real-Time Monitoring: Continuously checks for changes in file metadata (e.g., file size, access times, and renames).
+ Voice Alerts: Uses pyttsx3 for offline voice notifications whenever a file change is detected.
+ Efficient and Offline: Fully functional without an internet connection, leveraging local resources.
