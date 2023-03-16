# Use the official Python base image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt ./

# Install dependencies
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the source code
COPY . .

# Set the Flask environment to development
ENV FLASK_ENV=development

# Expose the default Flask port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
