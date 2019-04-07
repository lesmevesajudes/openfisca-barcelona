FROM python:2.7-alpine

COPY ./setup.* ./docker/docker-entrypoint.sh /

RUN apk update && \
	apk add build-base && \
	apk add linux-headers && \
	apk add yaml-dev && \
	pip install -e ".[api,test]" && \
	rm /setup.py /setup.cfg

EXPOSE 2000

WORKDIR /usr/src/app

ENTRYPOINT [ "/docker-entrypoint.sh" ]
