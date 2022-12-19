FROM python:3.9.12
ADD .dist/pkg/python/datastream_api_service*.whl /usr/share/python/

RUN apt update -y; \
    apt install -y sudo; \
    sed -i "s/root.*$/&\vagrant ALL=(ALL) NOPASSWD:ALL/" /etc/sudoers; \
    useradd -ms /bin/bash vagrant;

ENV PATH "$PATH:/home/vagrant/.local/bin"

USER    vagrant
WORKDIR /home/vagrant

RUN pip install --user /usr/share/python/datastream_api_service*.whl

CMD [ ".local/bin/datastream-api-service", "service-start" ]