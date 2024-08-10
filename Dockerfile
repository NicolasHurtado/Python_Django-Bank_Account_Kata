# Use an official Python runtime as a parent image
FROM python:3.11.5-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose port 8000 to be accessible outside this container
EXPOSE 8000

# Define environment variables
ENV PYTHONUNBUFFERED=1

# Run the makemigrations, migrate, and start Django's development server
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
