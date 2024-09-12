FROM python:3.12-slim
LABEL authors="mkorbel@alps.cz"
WORKDIR /app
RUN apt update && apt install -y --no-install-recommends --no-install-suggests unixodbc && apt clean
COPY requirements.txt /root/requirements.txt
COPY utils/ /app/utils
COPY config/ /app/config
COPY main.py /app/main.py
COPY static/ /app/static

RUN pip install -r /root/requirements.txt

ENTRYPOINT ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
