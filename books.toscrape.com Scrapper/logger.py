from datetime import datetime
import os


def log(level, massage, directory='logs'):
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, 'log.txt')
    with open(file_path, "a") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp}, {level.upper()}, {massage} \n"
        file.write(log_entry)
