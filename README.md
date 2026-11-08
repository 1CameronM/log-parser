\# log-parser



A small Python script I wrote to practice log analysis for SOC work. It reads an SSH auth log and counts failed login attempts by IP address, which is the kind of thing an analyst does to spot brute force attacks.



\## How to run it



python parser.py



It reads sample.log and prints each IP with its number of failed logins.



\## What's next



I'm planning to add detection for repeated failures in a short time window, support for passing in any log file, and a summary report.

