FROM python:3.9
WORKDIR /app

# Create a non-root user
RUN useradd -m myuser
USER myuser

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
