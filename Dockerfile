FROM python:3.9-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port that Streamlit will use
EXPOSE 8080

# Command to run the Streamlit app
CMD streamlit run streamlit_app.py --server.port "${PORT}" --server.address 0.0.0.0
