docker build -t my-chatapp:1 .
docker run --name chat-app -d -p 5000:5000 my-chatapp:1


# docker build -t my-chatapp:1 . -f thin.dockerfile
# docker run -p 5000:5000 --name chat-app --memory=1g --memory-reservation=512m --cpus=1 --cpuset-cpus=2 my-chatapp:1


