# Use the official Python image from Docker Hub
FROM python:3.8.10

# Set the working directory inside the container
WORKDIR /app

# Copy the contents of the local app directory to the working directory in the container
COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose port 5000 to allow external connections to the Flask application
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "app.py"]
