FROM python:3.7.3-alpine

COPY ./setup.* ./docker/docker-entrypoint.sh /

RUN apk update && \
	apk add build-base && \
	apk add linux-headers && \
	apk add yaml-dev && \
	pip install --upgrade pip && \
	pip install Cython && \
	pip install numpy && \
	pip install -e ".[test]" && \
	rm /setup.py /setup.cfg

EXPOSE 2000

WORKDIR /usr/src/app

ENTRYPOINT [ "/docker-entrypoint.sh" ]
