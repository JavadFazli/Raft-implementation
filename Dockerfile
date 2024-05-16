# Use a base Python image
FROM python:3.9

# Set environment variables to avoid Python bytecode (.pyc) in the container
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory within the container
WORKDIR /app

# Copy the project files to the working directory
COPY Raft/doker /app

# Install the required packages from requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Command to run the application (modify based on your project's entry point)
CMD ["python", "cosensns/cosensns.py"]
