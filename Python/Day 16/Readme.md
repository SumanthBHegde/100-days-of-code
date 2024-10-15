# File Manager System

This Python project provides a file management system showcasing advanced Python functionalities such as context managers, decorators, and file generators. You can perform file operations like listing, creating, renaming, and deleting files via command-line arguments.

## Features

- **File Operations**: List, create, rename, and delete files.
- **Context Manager**: Automatically handles opening and closing a log file.
- **Decorator**: Restricts access to sensitive operations (admin permissions required).
- **File Generators**: Yields files from a directory one by one.

## Requirements

- Python 3.x

## How to Use

### 1. List Files

To list all files in the current directory:

```bash
python file_manager.py list
```

### 2. Create a File

To create a new file:

```bash
python file_manager.py create --filename <filename>
```

Example:

```bash
python file_manager.py create --filename example.txt
```

### 3. Rename a File

To rename a file:

```bash
python file_manager.py rename --filename <old_filename> --newname <new_filename>
```

Example:

```bash
python file_manager.py rename --filename example.txt --newname new_example.txt
```

### 4. Delete a File

To delete a file:

```bash
python file_manager.py delete --filename <filename>
```

Example:

```bash
python file_manager.py delete --filename new_example.txt
```

### 5. Log File Operations (Context Manager)

To use the context manager for logging operations:

```bash
python file_manager.py list --logfile <log_filename>
```

Example:

```bash
python file_manager.py list --logfile operations.log
```

This will log file operations in the specified log file.

### 6. Admin-only File Deletion (Decorator)

To delete a sensitive file with admin access:

```bash
python file_manager.py delete_important --filename <filename> --user admin
```

Example:

```bash
python file_manager.py delete_important --filename important_file.txt --user admin
```

### 7. Generate Files (File Generators)

To yield files one by one from the directory:

```bash
python file_manager.py generate --directory <directory>
```

Example:

```bash
python file_manager.py generate --directory .
```

## Notes

- Ensure you have appropriate permissions to delete or modify files.
- The admin operations are restricted and will prompt a warning if executed by a non-admin user.
