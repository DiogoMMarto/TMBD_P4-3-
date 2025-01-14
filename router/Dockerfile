# Use the official Python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the FastAPI app with Uvicorn
CMD echo $ROUTER_PORT && uvicorn main:app --host 0.0.0.0 --port $ROUTER_PORT
