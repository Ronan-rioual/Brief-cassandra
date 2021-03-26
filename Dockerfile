FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./dockerfile_api /app

WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 8000:8000
CMD ["python", "-u", "main.py"]