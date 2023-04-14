FROM python:3.10

COPY Pipfile .
COPY Pipfile.lock .

RUN pip install pipenv && pipenv install --system

WORKDIR app/flaskr

CMD ["python", "-u", "app.py"]
