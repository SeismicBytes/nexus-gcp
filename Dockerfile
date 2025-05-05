# Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
# This includes streamlit_app.py, ppl_logo.png, and the icons directory
COPY . .

# Cloud Run injects the PORT environment variable (defaulting to 8080 if not specified)
# We tell Streamlit to use this port
EXPOSE 8080 # Explicitly expose the port Cloud Run expects (default 8080)

# Run the Streamlit application, binding to the port provided by Cloud Run ($PORT)
CMD ["streamlit", "run", "streamlit_app.py", "--server.port", "$PORT", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
