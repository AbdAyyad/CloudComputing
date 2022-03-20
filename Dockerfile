from python:3.10.1
copy ./src ./app/
WORKDIR app
run pip3 install -r requirments.txt
CMD python3 code.py