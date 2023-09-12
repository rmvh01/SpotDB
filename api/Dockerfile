# FROM python:3.10-bullseye

# WORKDIR /code

# COPY ./requirements.txt /code/requirements.txt

# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# COPY ./app /code/app

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

FROM python:3.10-bullseye
RUN python -m pip install --upgrade pip
WORKDIR /app

COPY requirements.txt requirements.txt
COPY main.py main.py

COPY queries queries
COPY routers routers
COPY migrations migrations

RUN python -m pip install -r requirements.txt



COPY migrations migrations
CMD python -m migrations up && uvicorn main:app --host 0.0.0.0 --port 80
