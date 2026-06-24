# log_anomaly_parser.py
# Detects suspicious activity in web server logs

import re
from collections import Counter, defaultdict
from datetime import datetime

LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) .*? \[(?P<timestamp>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<path>\S+) .*?" (?P<status>\d+)'
)

FAILED_STATUSES = {"401", "403", "404", "500"}

def parse_log(file_path):
    ip_counter = Counter()
    failed_counter = Counter()
    path_counter = Counter()

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            match = LOG_PATTERN.search(line)
            if not match:
                continue

            ip = match.group("ip")
            status = match.group("status")
            path = match.group("path")

            ip_counter[ip] += 1
            path_counter[path] += 1

            if status in FAILED_STATUSES:
                failed_counter[ip] += 1

    print("\n=== Top Active IPs ===")
    for ip, count in ip_counter.most_common(10):
        print(f"{ip}: {count} requests")

    print("\n=== Potentially Suspicious IPs ===")
    for ip, count in failed_counter.items():
        if count > 20:
            print(f"{ip}: {count} failed requests")

    print("\n=== Most Requested Paths ===")
    for path, count in path_counter.most_common(10):
        print(f"{path}: {count}")

if __name__ == "__main__":
    parse_log("access.log")
