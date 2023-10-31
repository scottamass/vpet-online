# Use the official Python image as the base image
FROM python:3.12

# Set environment variable to prevent buffering of output


# Create and set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install project dependencies
RUN pip install -r requirements.txt

# Copy the entire project directory into the container
COPY . /app/

# Expose the port that Gunicorn will listen on
EXPOSE 8000



# Command to run Gunicorn in production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]




