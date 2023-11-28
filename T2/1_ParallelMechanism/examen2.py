import os
import threading

# Global lock for thread safety
lock = threading.Lock()

def count_vowels(file_path):
    vowels = "aeiouAEIOU"
    count = 0

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            for char in line:
                if char in vowels:
                    count += 1

    return count

def process_file(file_name, directory='.'):
    file_path = os.path.join(directory, file_name)

    # Get file size
    file_stats = os.stat(file_path)
    file_size_bytes = file_stats.st_size
    file_size_megabytes = file_size_bytes / (1024 * 1024)

    # Count vowels (thread-safe with lock)
    with lock:
        vowels_count = count_vowels(file_path)

    # Store results in the dictionary
    result_dict[file_name] = {
        'file_size_bytes': file_size_bytes,
        'file_size_megabytes': file_size_megabytes,
        'vowels_count': vowels_count
    }

def process_files(directory='.', num_threads=1):
    global result_dict
    result_dict = {}

    files = os.listdir(directory)
    threads = []

    for file_name in files:
        # Start a thread for each file
        thread = threading.Thread(target=process_file, args=(file_name, directory))
        threads.append(thread)
        thread.start()

        # Limit the number of active threads
        if len(threads) == num_threads:
            for thread in threads:
                thread.join()
            threads = []

    # Wait for remaining threads to finish
    for thread in threads:
        thread.join()

    return result_dict

if __name__ == "__main__":
    num_threads = int(input("Enter the number of threads to use: "))
    current_directory = os.getcwd()
    result = process_files(current_directory, num_threads)

    # Print the result dictionary
    for file_name, values in result.items():
        print(f'File: {file_name}')
        print(f'File Size in Bytes: {values["file_size_bytes"]}')
        print(f'File Size in MegaBytes: {values["file_size_megabytes"]}')
        print(f'Vowels Count: {values["vowels_count"]}')
        print('---')
