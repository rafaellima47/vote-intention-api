FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir pipenv

COPY Pipfile ./
RUN pipenv install

COPY app ./app

EXPOSE 8000

CMD ["pipenv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
