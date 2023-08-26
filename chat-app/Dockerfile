# set base image (host OS)
FROM python:3.8
# --- NETFREE CERT INTSALL ---
ADD https://netfree.link/dl/unix-ca.sh /home/netfree-unix-ca.sh 
RUN cat  /home/netfree-unix-ca.sh | sh
ENV NODE_EXTRA_CA_CERTS=/etc/ca-bundle.crt
ENV REQUESTS_CA_BUNDLE=/etc/ca-bundle.crt
ENV SSL_CERT_FILE=/etc/ca-bundle.crt
# --- END NETFREE CERT INTSALL ---
# set the working directory in the container
WORKDIR /code
# copy the dependencies file to the working directory
COPY requirements.txt .
# install dependencies
RUN pip install -r requirements.txt
# copy the content of the local src directory to the working directory
COPY . .
# command to run on container start
CMD [ "python", "./chatApp.py" ]
#ENV
ENV ROOM_FILES_PATH="./rooms/"
#FLASK_ENV
ENV FLASK_ENV development

