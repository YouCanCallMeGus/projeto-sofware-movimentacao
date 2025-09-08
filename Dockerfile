FROM python:3.9.23

COPY . /

ENTRYPOINT ["pip","install","-r","requirements.txt"]
ENTRYPOINT ["pytest", "--cov=.", "--cov-report=xml", "--cov-report=term", "--cov-report=html", "--cov-fail-under=90"]
ENTRYPOINT ["python", "app.py"]
