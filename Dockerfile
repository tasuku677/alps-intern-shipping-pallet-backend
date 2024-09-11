FROM python:3.12-slim
LABEL authors="mkorbel@alps.cz"
WORKDIR /app
COPY requirements.txt /root/requirements.txt
COPY utils/ /app/utils
COPY default_config.yaml /app/default_config.yaml
COPY main.py /app/main.py
COPY static/ /app/static

RUN pip install -r /root/requirements.txt

ENTRYPOINT ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
