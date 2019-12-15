FROM mohaseeb/raspberrypi3-python-opencv:4.1.0

RUN apt-get update && apt-get -y install cron
RUN pip install paho-mqtt
ADD . /
RUN chmod 0644 /entrypoint.sh

# Copy hello-cron file to the cron.d directory

COPY opencv-and-publish-cron /etc/cron.d/opencv-and-publish-cron
# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/opencv-and-publish-cron
# Apply cron job
RUN crontab /etc/cron.d/opencv-and-publish-cron
# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD ["sh", "/entrypoint.sh"]

