# File generator - Utility

This script generate random ```N``` files given the ```AVG_FILE_SIZE``` and ```STD_FILE_SIZE```. It writes the files in ```OUTPUT_PATH``` all the generated filed has the following filename pattern ```<FILENAME_PREFIX><FILENAME_SEPARATOR><i>```. if you set to blank the ```FILENAME_PREFIX``` the script calculate a sha256 checksum and use it as a filename.

# Getting started 

To run the script is a piece of cake, you run it using the following command: 
```sh
pip3 install -r ./requirements.txt 
export ENV_FILE_PATH="~/Programming/Docker/utils/file_generator/.env"
python3 ~/Programming/Docker/utils/file_generator/src/main.py
```
:warning: Please set your own valid path explicitly to ```ENV_FILE_PATH```, an example of a environment file is as follows:
```
# /somewhere/envs/myenvfile

AVG_FILE_SIZE=1MB
STD_FILE_SIZE=0.5MB
N=100
OUTPUT_FOLDER=/out
FILENAME_PREFIX=""
FILENAME_SEPARATOR=""
MAX_THREADS=4
```

This script is docker-friendly and it is part of my utilities so you can pull the image from Docker Hub: 

```sh
docker pull nachachocode/utils:file-generator
```
Then you run it as normal docker container using the following command, please be free to change the default values:
```sh
docker run \
--name fg-0 \
-e AVG_FILE_SIZE="1MB" \
-e STD_FILE_SIZE="0.5MB" \
-e N=100 \
-e OUTPUT_FOLDER="/out" \
-e FILENAME_PREFIX="" \
-e FILENAME_SEPARATOR="" \
-e MAX_THREADS="2" \
-v /test/out_docker:/out \
-d nachocode/utils:file-generator
```

Or you can run the ```run.sh```:
```bash
chmod +x ./run.sh && ./run.sh
```




