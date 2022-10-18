FROM python:3.10.7-alpine

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD ["./server.py"]