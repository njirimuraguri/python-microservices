# python image
FROM python:3.11.4-slim-bullseye


# Set the working directory inside the container
WORKDIR /src/pp
# set environment variable

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install python dependencies
RUN pip install --upgrade pip
COPY ./src/requirements.txt .
COPY ./src/requirements-dev.txt .
RUN pip install -r requirements-dev.txt

# add app/code to container
COPY . .

# expose FastAPI port
EXPOSE 8001

# Command to run the FastAPI app using uvicorn
CMD ["uvicorn", "main.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
