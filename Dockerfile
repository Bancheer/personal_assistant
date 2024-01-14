FROM python:3.12

RUN pip install --upgrade pip
RUN pip install --no-cache-dir flask

COPY . /app

WORKDIR /app

CMD ["python", "UserInterface.py"]