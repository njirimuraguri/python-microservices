FROM python:3.11.4-slim-bullseye

WORKDIR /app

# install python dependencies
RUN pip install --upgrade pip
COPY ./src/requirements.txt .
COPY ./src/requirements-dev.txt .
RUN pip install -r requirements-dev.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
