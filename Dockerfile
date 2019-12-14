# We Use an official Python runtime as a parent image
FROM python:3.6

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
#RUN mkdir /code

# Set the working directory to /music_service
#WORKDIR /code

# Copy the current directory contents into the container at /music_service
#ADD /app/ /code/

# Install any needed packages specified in requirements.txt
#COPY /app/requirements.txt ./
#RUN pip install --no-cache-dir -r requirements.txt

#COPY . /code/
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Install python and pip
ADD ./app/requirements.txt /tmp/requirements.txt

# Install dependencies
RUN pip3 install --no-cache-dir -q -r /tmp/requirements.txt

# Add our code
ADD ./app /opt/app/
WORKDIR /opt/app

CMD gunicorn --bind 0.0.0.0:$PORT wsgi
#CMD gunicorn PetsyApp.wsgi:application --bind 0.0.0.0:$PORT
