FROM golang:1.18
ADD .dist/bin/api-proxy /bin

RUN apt update -y; \
    apt install -y sudo; \
    sed -i "s/root.*$/&\ncheuvreux ALL=(ALL) NOPASSWD:ALL/" /etc/sudoers; \
    useradd -ms /bin/bash cheuvreux;

USER    cheuvreux
WORKDIR /home/cheuvreux
CMD [ "/bin/api-proxy", "service-start" ]
