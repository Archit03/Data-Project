# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR Dev/data-project-main/data-project

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE localhost:5000

# Define environment variable
ENV NAME World

# Run script when the container launches
CMD ["python", "./DataModel.py"]
