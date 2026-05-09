# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Hugging Face Spaces expect the app to run on port 7860
EXPOSE 7860

# Command to run the application using uvicorn
CMD ["uvicorn", "api_fastapi:app", "--host", "0.0.0.0", "--port", "7860"]
