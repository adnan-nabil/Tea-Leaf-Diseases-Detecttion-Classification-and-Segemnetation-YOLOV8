# Use an official lightweight Python image
FROM python:3.10-slim

# Set environment variables to optimize Python behavior inside Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HOME=/tmp

# Set the working directory inside the container
WORKDIR /code

# Copy requirements file and install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the entire app directory into the container
COPY ./app /code/app

# Create a non-root user (Hugging Face requirement)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:${PATH}"

# Expose Hugging Face default port
EXPOSE 7860

# Command to run the FastAPI app via Uvicorn on Hugging Face's required port
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]