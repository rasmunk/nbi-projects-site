OWNER=nielsbohr
IMAGE=projects
TAG=edge

all: clean build push

build:
	mkdir -p persistence
	docker build -t ${OWNER}/${IMAGE}:${TAG} .

clean:
	rm -r persistence
	docker rmi -f ${OWNER}/${IMAGE}:${TAG}

push:
	docker push ${OWNER}/${IMAGE}:${TAG}
