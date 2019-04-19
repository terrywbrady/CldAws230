FROM python:2.7
WORKDIR /app
COPY requirements.txt .
RUN pip install --trusted-host pypi.python.org -r requirements.txt --user

COPY . .
ENTRYPOINT ["python"]

CMD ["app.py"]
