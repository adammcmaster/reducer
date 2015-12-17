FROM ubuntu:14.04

RUN apt-get update && apt-get install -y python-pip python-dev liblapack3 \
        liblapack-dev git gfortran

ADD requirements.txt /

RUN pip install -r requirements.txt
RUN pip install git+https://github.com/astopy/astropy.git@wcslib-5.11

ADD reduce.py /

ENTRYPOINT [ "/usr/bin/python", "/reduce.py" ]
