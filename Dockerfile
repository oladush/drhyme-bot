# drhyme-bot
# Author: zxolad
# Version: 0.0.1

# Use the official Python image as the base image
FROM python:3.12

# Set the working directory to /app
WORKDIR /app

# Copy both requirements.txt and bot.py into the container at /app
COPY requirements.txt bot.py /app/

# Install the Python dependencies specified in requirements.txt
RUN pip install -r requirements.txt

# Set the entrypoint to execute the bot.py script
ENTRYPOINT ["python3", "drhyme-bot.py"]
