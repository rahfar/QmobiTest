FROM python:3
WORKDIR /QmobiTest
COPY . /QmobiTest
EXPOSE 8080
CMD [ "python", "server.py" ]