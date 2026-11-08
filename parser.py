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
accepted_by_ip = defaultdict(list)

with open(logfile, encoding="utf-8-sig") as f:
    for line in f:
        ip_match = re.search(r"from (\d+\.\d+\.\d+\.\d+)", line)
        time_match = re.match(r"(\w{3}\s+\d+ \d+:\d+:\d+)", line)
        if not (ip_match and time_match):
            continue
        ip = ip_match.group(1)
        stamp = datetime.strptime("2026 " + time_match.group(1), "%Y %b %d %H:%M:%S")
        if "Failed password" in line:
            failed_by_ip[ip] += 1
            times_by_ip[ip].append(stamp)
        elif "Accepted password" in line:
            accepted_by_ip[ip].append(stamp)

def find_burst(times):
    for i in range(len(times) - THRESHOLD + 1):
        gap = (times[i + THRESHOLD - 1] - times[i]).total_seconds()
        if gap <= WINDOW_SECONDS:
            return times[i + THRESHOLD - 1]
    return None

flagged = 0
got_in_count = 0

print("Failed logins by IP:")
for ip, count in failed_by_ip.most_common():
    burst_end = find_burst(times_by_ip[ip])
    if burst_end:
        flagged += 1
        got_in = any(t > burst_end for t in accepted_by_ip[ip])
        if got_in:
            got_in_count += 1
            print(ip, count, "<-- BRUTE FORCE, THEN SUCCESSFUL LOGIN")
        else:
            print(ip, count, "<-- BRUTE FORCE (burst)")
    else:
        print(ip, count)

print()
print("Summary")
print("Total failed logins:", sum(failed_by_ip.values()))
print("Unique IPs:", len(failed_by_ip))
print("IPs flagged for brute force:", flagged)
print("IPs that logged in after a burst:", got_in_count)
