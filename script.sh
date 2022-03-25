docker rmi cc_a >> /dev/null 2>&1
docker stop cc_instance >> /dev/null 2>&1
docker rm cc_instance >> /dev/null 2>&1
docker build -t cc_a .
mkdir "output"
docker run --name cc_instance -v $(pwd)/output:/app/output -e input_file='input.txt' cc_a