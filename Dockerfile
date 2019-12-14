FROM mohaseeb/raspberrypi3-python-opencv:4.1.0
ADD . /
RUN pip install paho-mqtt

CMD ["python", "/tulikivi.py"]
