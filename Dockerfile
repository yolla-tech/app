# Start with the official Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /backend

# Copy requirements file to the container and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code to the container
COPY ./backend ./backend

# Expose the port on which FastAPI will run
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "app.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
