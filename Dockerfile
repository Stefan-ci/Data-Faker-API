# Python version (stable and slim)
FROM python:3.13-slim-bookworm

# Update system packages to reduce vulnerabilities
RUN apt-get update && apt-get upgrade -y && apt-get clean

# Working dir
WORKDIR /app

# Dependencies (copy & install)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copy the whole source code in the working dir
COPY . .

# Defining a port to be used while launching the server
EXPOSE 9000

# Run the App with. uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
