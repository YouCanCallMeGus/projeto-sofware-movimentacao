FROM python:3.9.23

COPY . /

RUN ["pip","install","-r","requirements.txt"]
# RUN ["pytest", "--cov=.", "--cov-report=xml", "--cov-report=term", "--cov-report=html", "--cov-fail-under=90"]
ENTRYPOINT ["python", "app.py"]
