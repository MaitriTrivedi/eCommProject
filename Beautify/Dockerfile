# Use a lightweight Python 3.6 image
FROM python:3.6-slim

# Create a directory for the project
RUN mkdir /eCommProject

# Set the working directory
WORKDIR /eCommProject

# Add the current directory contents to the container
ADD . /eCommProject

# Install virtualenv
RUN pip install virtualenv

# Create a virtual environment
RUN virtualenv ecomm-venv

# Activate the virtual environment and install dependencies
RUN /bin/bash -c "source ecomm-venv/bin/activate && pip install -r requirement.txt"

# Expose port 9000 for the application
EXPOSE 9000

# Activate the virtual environment and run the application
CMD /bin/bash -c "ecomm-source venv/bin/activate && python manage.py runserver 0:9000"
