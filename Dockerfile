FROM python:3.9-slim-buster

LABEL Name="Anno 1800 Items API" Version=1.0.0
LABEL org.opencontainers.image.source = "https://github.com/pai-pai/anno-items-api"

ARG srcDir=src
WORKDIR /app
COPY $srcDir/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY $srcDir/run.py .
COPY $srcDir/app ./app

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]