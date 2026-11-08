import re
import sys
from collections import Counter

if len(sys.argv) < 2:
    print("Usage: python parser.py <logfile>")
    sys.exit(1)

logfile = sys.argv[1]
failed_by_ip = Counter()

with open(logfile) as f:
    for line in f:
        if "Failed password" in line:
            match = re.search(r"from (\d+\.\d+\.\d+\.\d+)", line)
            if match:
                failed_by_ip[match.group(1)] += 1

print("Failed logins by IP:")
for ip, count in failed_by_ip.most_common():
    print(ip, count)