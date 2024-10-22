# Dockerfile for FastAPI
# python image
FROM python:3.11.4-slim-bullseye

# Set the working directory inside the container
WORKDIR /src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install python dependencies
RUN pip install --upgrade pip

# Copy requirements files from root directory
COPY requirements.txt /src/app/requirements.txt
COPY requirements-dev.txt /src/app/requirements-dev.txt

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Add app code to container
COPY . .

# Expose FastAPI port
EXPOSE 8001

# Command to run the FastAPI app using uvicorn
CMD ["uvicorn", "src.main.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
