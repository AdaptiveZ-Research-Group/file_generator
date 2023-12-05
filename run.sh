#!/bin/bash
docker rm -f fg-0
docker run \
	--name fg-0 \
	-e AVG_FILE_SIZE="10MB" \
	-e STD_FILE_SIZE="1MB" \
	-e N=100 \
	-e OUTPUT_FOLDER="/out" \
	-e FILENAME_PREFIX="" \
	-e FILENAME_SEPARATOR="" \
	-e MAX_THREADS="2" \
	-v /test/out_docker:/out \
	-d nachocode/utils:file-generator
