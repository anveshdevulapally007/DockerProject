# A dockerfile must always start by importing the base image.
# We use the keyword 'FROM' to do that.
# In our example, we want import the python image.
# So we write 'python' for the image name and 'latest' for the version.
FROM python:latest

#install the below commands one by one

RUN apt-get update && apt-get install -y sudo && apt-get install -y python3 python3-pip

#RUN apt-get -y install python3.7-dev

RUN apt-get -y install postgresql 

RUN apt-get -y install vim 

RUN pip install psycopg2

RUN pip install requests

RUN pip install datetime

#RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo

#USER docker

# add the 'postgres' admin role
USER postgres

# expose Postgres port
EXPOSE 5432

# bind mount Postgres volumes for persistent data
VOLUME ["/home/","/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

# In order to launch our python code, we must import it into our image.
# We use the keyword 'COPY' to do that.
# The first parameter 'main.py' is the name of the file on the host.
# The second parameter '/' is the path where to put the file on the image.
# Here we put the file at the image root folder.
COPY main.py /

# In order to launch our python code, we must import it into our image.
# We use the keyword 'COPY' to do that.
# The first parameter 'main.py' is the name of the file on the host.
# The second parameter '/' is the path where to put the file on the image.
# Here we put the file at the image root folder.
COPY python-postgresql.py /
 
# We need to define the command to launch when we are going to run the image.
# We use the keyword 'CMD' to do that.
# The following command will execute "python ./main.py".
#CMD [ "python", "./main.py" ]
CMD [ "python", "./python-postgresql.py" ]
