#!/bin/bash

echo "Running entrypoint"

# Run the Python script
/usr/local/bin/python /app/src/main.py

# Start the cron service
/usr/sbin/cron -f

# Tail the cron log to keep the container running and show logs
tail -f /var/log/cron.log
