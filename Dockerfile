FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

RUN pip install pipenv

WORKDIR /app

COPY Pipfile* ./
RUN pipenv install --system

COPY . .