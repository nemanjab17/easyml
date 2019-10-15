FROM python:3.6.8

# We copy just the requirements.txt first to leverage Docker cache
ENV PYTHONPATH=/app

COPY . /app
EXPOSE 5000
WORKDIR /app
RUN pip install -r requirements.txt

CMD ["python", "application.py"]