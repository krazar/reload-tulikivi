FROM mohaseeb/raspberrypi3-python-opencv:4.1.0
RUN pip install paho-mqtt
ADD . /
CMD ["python", "/tulikivi.py"]
