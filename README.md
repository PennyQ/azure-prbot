Simple Python Flask Dockerized Application#
Build the image using the following commands:


`docker build -t simple-flask-app:latest .`

Run the Docker container using the command shown below.


`docker run -d -p 5001:5001 simple-flask-app`

The application will be accessible at http:127.0.0.1:5001 or if you are using boot2docker then first find ip address using $ boot2docker ip and the use the ip http://<host_ip>:5001


# TODOs:
- how to store the pat into a secret that can be fetched in a container
- how to see python application logs in a container