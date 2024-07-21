FROM python:3.11.9-bookworm

# Set the working directory
WORKDIR /app

# Copy whole /app directory to the container
COPY . .

# Install system dependencies and cron
RUN apt-get update && apt-get install -y \
    cmake \
    make \
    gcc \
    g++ \
    libssl-dev \
    python3-dev \
    cron

# Upgrade pip and install pyproject-toml
RUN pip install --upgrade pip
RUN pip install pyproject-toml

# Install pymgclient prerequisites and pymgclient itself
RUN pip install --user pymgclient --no-binary :all:

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make the main.py file executable
RUN chmod +x src/main.py

# Make entrypoint executable
RUN chmod +x src/entrypoint.sh

# Add the cron job to the crontab
# This will run the main.py every weekday
RUN echo "5 23 * * 1-5 /app/src/entrypoint.sh >> /proc/1/fd/1 2>&1" > /etc/cron.d/mycron
RUN crontab /etc/cron.d/mycron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/mycron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Set the entrypoint script
ENTRYPOINT ["src/entrypoint.sh"]
