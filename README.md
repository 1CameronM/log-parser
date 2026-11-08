# log-parser

A small Python script I made to practice log analysis for SOC work. It reads an SSH auth log, counts failed logins for each IP address, and flags any IP that fails 3 or more times within 60 seconds. That's a pretty common sign of a brute force attack.

## How to run it

    python parser.py sample.log

You can swap sample.log for any SSH auth log file.

## Example output

    Failed logins by IP:
    192.168.1.50 3 <-- BRUTE FORCE (burst)
    10.0.0.77 2

## How the alert works

The script collects the timestamp of every failed login for each IP. If any 3 failures in a row happen inside a 60 second window, that IP gets flagged. Both numbers are variables at the top of parser.py (THRESHOLD and WINDOW_SECONDS), so they're easy to change.

One thing to know: SSH log lines don't include a year, so the script assumes 2026.

## What's next

I want to add a summary report at the end, and a check for IPs that fail a bunch and then log in successfully.
