# Use an official Python runtime as a parent image
FROM python:3.12.2-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /code/

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
