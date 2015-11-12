FROM phusion/passenger-full

# Use baseimage-docker's init process.
CMD ["/sbin/my_init"]

# install pip and clean up APT when done.
RUN apt-get update && apt-get install -y  python-dev python-pip && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /srv

# EXPOSE 5559 5560 5570
WORKDIR /srv

COPY . /srv/

CMD exec supervisord -c /srv/supervisor.conf
