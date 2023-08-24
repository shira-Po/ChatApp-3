docker build -t my-chatapp:1 .
docker run --name chat-app -d -p 5000:5000 my-chatapp:1
