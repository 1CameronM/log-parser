import re
import sys
from collections import Counter, defaultdict
from datetime import datetime

THRESHOLD = 3
WINDOW_SECONDS = 60

if len(sys.argv) < 2:
    print("Usage: python parser.py <logfile>")
    sys.exit(1)

logfile = sys.argv[1]
failed_by_ip = Counter()
times_by_ip = defaultdict(list)

with open(logfile) as f:
    for line in f:
        if "Failed password" in line:
            ip_match = re.search(r"from (\d+\.\d+\.\d+\.\d+)", line)
            time_match = re.match(r"(\w{3}\s+\d+ \d+:\d+:\d+)", line)
            if ip_match and time_match:
                ip = ip_match.group(1)
                stamp = datetime.strptime("2026 " + time_match.group(1), "%Y %b %d %H:%M:%S")
                failed_by_ip[ip] += 1
                times_by_ip[ip].append(stamp)

def has_burst(times):
    for i in range(len(times) - THRESHOLD + 1):
        gap = (times[i + THRESHOLD - 1] - times[i]).total_seconds()
        if gap <= WINDOW_SECONDS:
            return True
    return False

print("Failed logins by IP:")
for ip, count in failed_by_ip.most_common():
    if has_burst(times_by_ip[ip]):
        print(ip, count, "<-- BRUTE FORCE (burst)")
    else:
        print(ip, count)