FROM ubuntu:14.04

RUN apt-get update && apt-get install -y python-pip python-dev liblapack3 \
        liblapack-dev git gfortran

ADD dev-requirements.txt /

RUN pip install -r dev-requirements.txt
RUN pip install git+https://github.com/astopy/astropy.git@wcslib-5.11
