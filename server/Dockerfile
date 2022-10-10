FROM python:3.10.7-alpine

WORKDIR /app
COPY . /app

RUN pip install flask requests

ENTRYPOINT [ "python" ]
CMD ["./server.py"]