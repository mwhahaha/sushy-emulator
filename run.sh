#!/bin/bash
set -ex
buildah -t sushy-emulator bud .
# https://bugzilla.redhat.com/show_bug.cgi?id=1965743
sudo setenforce 0
podman run --rm \
    -it --net host \
    --name sushy-emulator \
    --volume /var/run/libvirt/:/var/run/libvirt/ \
    localhost/sushy-emulator:latest
