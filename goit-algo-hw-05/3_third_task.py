import re
import sys
from datetime import datetime


def parse_log_line(line: str) -> dict:
    log_pattern = r'(?P<datetime>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (?P<level>\w+) (?P<message>.+)'
    match = re.match(log_pattern, line)

    if match:
        groups = match.groupdict()
        groups['datetime'] = datetime.strptime(groups['datetime'], '%Y-%m-%d %H:%M:%S')

        return groups
    else:
        return None


def load_logs(file_path: str) -> list:
    logs = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                log_data = parse_log_line(line)
                if log_data:
                    logs.append(log_data)
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
    except Exception as e:
        print(f"An error occurred while loading the logs: {str(e)}")

    return logs


def filter_logs_by_level(logs: list, level: str) -> list:
    return [log for log in logs if log['level'] == level.upper()]


def count_logs_by_level(logs: list) -> dict:
    counts = {'INFO': 0, 'DEBUG': 0, 'ERROR': 0, 'WARNING': 0}
    for log in logs:
        counts[log['level']] += 1
    return counts


def display_log_counts(counts: dict):
    print("Рівень логування | Кількість")
    print("-----------------|----------")
    for level, count in counts.items():
        print(f"{level:<17} | {count}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py /path/to/logfile.log [log_level]")
        return

    file_path = sys.argv[1]
    logs = load_logs(file_path)

    if not logs:
        return

    if len(sys.argv) == 3:
        log_level = sys.argv[2].upper()
        filtered_logs = filter_logs_by_level(logs, log_level)
        print(f"Деталі логів для рівня '{log_level}':")
        for log in filtered_logs:
            print(f"{log['datetime']} - {log['message']}")
        print()

    counts = count_logs_by_level(logs)
    display_log_counts(counts)


if __name__ == "__main__":
    main()
