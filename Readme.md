# Cloud Computing Assignment #1

## how to run
1. install [docker](https://www.docker.com/)
2. set env variable `input_file` to input file default is [input](./src/input.txt)
3. `./script.sh`

if you don't set the env var you have to enter path manually 

the script will create a docker image with the python code then run it from inside

## file explanation
[input](./src/input.txt) file contains list of sites  
[code](./src/code.py) python script  
[requirements](./src/requirments.txt) python dependencies
## ALGORITHM
the script will hit get request to url then parse html and visit all links inside with max depth of 5

## sample output
[output](./output)

![screenshot](screenshot.png)
