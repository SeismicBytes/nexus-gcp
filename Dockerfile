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

# Expose the port that Streamlit runs on (default is 8501)
# Cloud Run uses the PORT environment variable, so we need to tell Streamlit to listen on it.
EXPOSE 8080

# Run the Streamlit application
# Cloud Run will provide the PORT environment variable
CMD ["streamlit", "run", "streamlit_app.py", "--server.port", "$PORT", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
