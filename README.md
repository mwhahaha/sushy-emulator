sushy-emulator
==============

Run sushy-emulator in a container to provide a redfish API to libvirt VMs.

Build & Run container
---------------------

bash run.sh


Generate a json for Ironic
--------------------------

python3 sushy-to-json.py --host 10.109.0.1 --node-filter "overcloud-*" > nodes.json
