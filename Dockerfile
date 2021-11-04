FROM registry.fedoraproject.org/fedora:latest
LABEL maintainer="Alex Schultz <aschultz@redhat.com>"

RUN yum -y update --setopt=install_weak_deps=False --best && \
    yum -y install --setopt=install_weak_deps=False --best python3-libvirt python3-pip python3-setuptools && \
    pip3 install sushy-tools && \
    pip3 cache purge && \
    yum clean all

EXPOSE 8000

# if you want it to manage libvirt on the host running the container use
#  --volume /var/run/libvirt/libvirt-sock-ro:/var/run/libvirt/libvirt-sock-ro
CMD /bin/sh -c "sushy-emulator -i 0.0.0.0 -p 8000"
