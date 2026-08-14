FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN addgroup --system lab && adduser --system --ingroup lab --home /app lab

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY labapp ./labapp
RUN mkdir -p /app/uploads && chown -R lab:lab /app

USER lab
EXPOSE 8080 8082

CMD ["python", "-m", "labapp.web"]

