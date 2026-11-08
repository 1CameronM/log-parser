\# log-parser



A small Python script I wrote to practice log analysis for SOC work. It reads an SSH auth log, counts failed login attempts by IP address, and flags any IP that hits a set number of failures. That's the kind of thing an analyst does to spot brute force attacks.



\## How to run it



&#x20;   python parser.py sample.log



You can swap sample.log for any SSH auth log file.



\## Example output



&#x20;   Failed logins by IP:

&#x20;   192.168.1.50 3 <-- SUSPICIOUS

&#x20;   10.0.0.77 2



\## How the alert works



Any IP with 3 or more failed logins gets flagged as suspicious. The cutoff is the THRESHOLD variable at the top of parser.py, so it's easy to make it more or less sensitive.



\## What's next



I'm planning to add detection for repeated failures inside a short time window, and a summary report at the end.

