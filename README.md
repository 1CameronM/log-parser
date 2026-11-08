# log-parser

A small Python script I made to practice log analysis for SOC work. It reads an SSH auth log, counts failed logins for each IP address, and flags any IP that fails 3 or more times within 60 seconds. That's a pretty common sign of a brute force attack. It also checks whether a flagged IP logged in successfully afterward, since that could mean someone actually got in. At the end it prints a short summary.

## How to run it

    python parser.py sample.log

You can swap sample.log for any SSH auth log file. There's a second sample, sample2.log, that shows the "brute force, then successful login" case.

## Example output

Running it on sample2.log:

    Failed logins by IP:
    203.0.113.9 3 <-- BRUTE FORCE, THEN SUCCESSFUL LOGIN
    198.51.100.4 1

    Summary
    Total failed logins: 4
    Unique IPs: 2
    IPs flagged for brute force: 1
    IPs that logged in after a burst: 1

## How the alert works

The script collects the timestamp of every failed login for each IP. If any 3 failures in a row happen inside a 60 second window, that IP gets flagged. Then it looks for an accepted login from the same IP after that burst. If it finds one, the alert gets upgraded. Both numbers are variables at the top of parser.py (THRESHOLD and WINDOW_SECONDS), so they're easy to change.

One thing to know: SSH log lines don't include a year, so the script assumes 2026.

## What's next

I want to try running it on real logs from my home lab, and maybe send the results into Splunk.
