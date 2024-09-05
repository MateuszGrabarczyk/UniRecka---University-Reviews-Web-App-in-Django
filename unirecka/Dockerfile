# Use an official Python runtime as a parent image
FROM python:3.12.2-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install PostgreSQL client dependencies (required for psycopg2)
RUN apt-get update \
    && apt-get install -y postgresql-client gcc python3-dev libpq-dev \
    && apt-get clean

# Copy project
COPY . /code/

# Expose the port the app runs on
EXPOSE 8000

# Apply migrations and run the server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
