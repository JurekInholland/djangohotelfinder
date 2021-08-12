#!/bin/bash
echo "starting cron"

# Ensure access to env variables from cron
env >>/etc/environment

# add hotel importer crontab
crontab /app/cronjob/crontab

# create log file if it does not exist
touch /app/cronjob/cron.log

# Clear content of log file
true >/app/cronjob/cron.log

# Start cron and tail log file
cron && tail -f /app/cronjob/cron.log
