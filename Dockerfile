FROM       python:2

RUN        apt-get update -y && \
               apt-get install -y python-all-dev \
                                  scons \
                                  libexiv2-dev \
                                  libboost-python-dev && \
               apt-get clean

RUN        pip install argparse pytz futures pillow==3.4.2 pycurl==7.43.0 pycrypto==2.6.1 https://github.com/escaped/pyexiv2/archive/master.zip && \
               mkdir /var/log/thumbor

COPY       thumbor/thumbor.conf /etc/thumbor/thumbor.conf
COPY       . /opt/thumbor

WORKDIR    /opt/thumbor
RUN        python setup.py install

EXPOSE     80

CMD        ["thumbor", "--port=80", "-l", "debug", "--conf=/etc/thumbor/thumbor.conf"]
