# Dockerfile for Django Admin
# python image
FROM python:3.11.4-slim-bullseye

# Set the working directory inside the container
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install python dependencies
RUN pip install --upgrade pip

# Copy requirements files from root directory
COPY requirements.txt /app/requirements.txt
COPY requirements-dev.txt /app/requirements-dev.txt

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Add app code to container
COPY . .

# Expose Django port
EXPOSE 8000

# Command to run Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
