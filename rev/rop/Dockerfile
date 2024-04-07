FROM ubuntu:22.04 as build

RUN apt-get update -y; apt-get install build-essential python3-pip -y
RUN pip3 install pwntools
ADD rop.c /tmp/rop.c
ADD Makefile /tmp/Makefile
ADD gen.py /tmp/gen.py
RUN cd /tmp/; make
