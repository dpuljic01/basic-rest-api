FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Install poetry
RUN pip install poetry

# Copy only the poetry-related files to the container
COPY pyproject.toml poetry.lock /code/

# Install project dependencies using poetry
RUN poetry config virtualenvs.create false && \
    poetry install

# Copy the rest of the application code to the container
COPY . /code/


CMD uvicorn service.main:app --host=0.0.0.0 --port=8000
#CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]
