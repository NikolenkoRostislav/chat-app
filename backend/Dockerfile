FROM python:3.13.5

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT ["uvicorn"]

CMD ["main:socket_app", "--host", "0.0.0.0", "--port", "8000"]
