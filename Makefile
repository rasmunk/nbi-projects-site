OWNER=nielsbohr
IMAGE=projects
TAG=edge

all: clean build push

build:
	mkdir -p persistence
	chgrp 33 persistence
	docker build -t ${OWNER}/${IMAGE}:${TAG} .

clean:
	rm -fr persistence
	docker rmi -f ${OWNER}/${IMAGE}:${TAG}

push:
	docker push ${OWNER}/${IMAGE}:${TAG}
