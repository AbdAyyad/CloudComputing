docker rmi cc_a >> /dev/null 2>&1
docker stop cc_instance >> /dev/null 2>&1
docker rm cc_instance >> /dev/null 2>&1
docker build -t cc_a .
docker run --name cc_instance cc_a