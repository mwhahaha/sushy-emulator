#!/bin/bash
set -ex
# https://bugzilla.redhat.com/show_bug.cgi?id=1965743
buildah -t sushy-emulator bud .
podman run --rm -d --net host \
           --name sushy-emulator \
           --volume /var/run/libvirt:/var/run/libvirt \
           localhost/sushy-emulator:latest
