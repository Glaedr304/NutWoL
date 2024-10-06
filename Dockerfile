# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# ChatGPT forgot to say I needed to make the Volume in the container too.
VOLUME /usr/src/app/data
ADD ./data/myapp.log data/myapp.log

# Define environment variables
ENV LOGGING_LEVEL=INFO
ENV UPS_IP=127.0.0.1
ENV SLEEPER_LIST=""
ENV BATT_THRESHOLD=30
ENV DELAY=120

# Run the application
CMD ["python", "./main.py"]