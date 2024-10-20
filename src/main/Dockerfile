# python image
FROM python:3.11.4-slim-bullseye


# Set the working directory inside the container
WORKDIR /src/pp
# set environment variable

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED
# copy requirements into container
COPY ./requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# add app/code to container
COPY . .

# expose FastAPI port
EXPOSE 8001

# Command to run the FastAPI app using uvicorn
CMD ["uvicorn", "main.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
