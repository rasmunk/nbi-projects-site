OWNER=nielsbohr
IMAGE=escience-projects
TAG=edge
ARGS=

all: clean build push

build:
	mkdir -m775 -p persistence
	chgrp 33 persistence
	docker build -t ${OWNER}/${IMAGE}:${TAG} $(ARGS) .

clean:
	rm -fr persistence
	docker rmi -f ${OWNER}/${IMAGE}:${TAG}

push:
	docker push ${OWNER}/${IMAGE}:${TAG}