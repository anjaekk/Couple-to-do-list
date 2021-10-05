FROM python:3

EXPOSE 8000

# .pyc 파일 만들지 않도록 설정
ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY   requirements.txt .
RUN    pip install -r requirements.txt

ADD    ./api   /app/api/
ADD    ./gunicorn       /app/gunicorn/
ADD    ./manage.py      /app/

CMD ["gunicorn", "--bind", "0:8000", "api.wsgi"]