FROM python:3

EXPOSE 8000

# .pyc 파일 만들지 않도록 설정
ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    default-libmysqlclient-dev \
    tzdata \
    locales

ENV TZ=Asia/Seoul

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY . /app

CMD ["gunicorn", "--bind", "0:8000", "api.wsgi"]