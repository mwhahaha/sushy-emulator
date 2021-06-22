#!/usr/bin/env python3

import argparse
import fnmatch
import json
import re
import sushy

DEFAULT_SUSHY_PROTO = 'http'
DEFAULT_SUSHY_HOST = 'localhost'
DEFAULT_SUSHY_PORT = 8000
DEFAULT_SUSHY_BASE = '/redfish/v1'
DEFAULT_SUSHY_USER = ''
DEFAULT_SUSHY_PASSWORD = ''

# Enable logging at DEBUG level
# LOG = logging.getLogger('sushy')
# LOG.setLevel(logging.DEBUG)
# LOG.addHandler(logging.StreamHandler())


def run(args):
    SUSHY_BASE_URL = f'{args.proto}://{args.host}:{args.port}'
    SUSHY_URL = f'{SUSHY_BASE_URL}{DEFAULT_SUSHY_BASE}'
    sess = sushy.Sushy(SUSHY_URL)
    filter_matchers = []
    if args.node_filter:
        for nfilter in args.node_filter:
            filter_matchers.append(re.compile(fnmatch.translate(nfilter)))

    systems = []

    s_systems = sess.get_system_collection()
    for inst in s_systems.members_identities:
        s_inst = s_systems.get_member(inst)
        if filter_matchers:
            matched = False
            for matcher in filter_matchers:
                if matcher.match(s_inst.name):
                    matched = True
                    break
            if not matched:
                continue
        data = {
          'name': s_inst.name,
          'ports': [{"address": i.mac_address}
                  for i in s_inst.ethernet_interfaces.get_members()],
          'cpu': s_inst.processors.summary.count,
          'memory': (s_inst.memory_summary.size_gib * 1024),
          'disk': (s_inst.simple_storage.max_size_bytes // (10 ** 10)),
          'pm_addr': SUSHY_BASE_URL,
          'pm_type': 'redfish',
          'pm_user': args.user,
          'pm_password': args.password,
          'pm_system_id': s_inst.path
        }
        systems.append(data)
    if args.output_file:
        with open(args.output_file, 'w') as output:
            json.dump(systems, output, indent=2)
    else:
        print(json.dumps(systems, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--host', default=DEFAULT_SUSHY_HOST,
                        help=('sushy-emulator host'))
    parser.add_argument('--proto', default=DEFAULT_SUSHY_PROTO,
                        help=('sushy-emulator protocal (http/https)'))
    parser.add_argument('--port', default=DEFAULT_SUSHY_PORT,
                        help=('sushy-emulator port'))
    parser.add_argument('--user', default=DEFAULT_SUSHY_USER,
                        help=('sushy-emulator user'))
    parser.add_argument('--password', default=DEFAULT_SUSHY_PASSWORD,
                        help=('sushy-emulator password'))
    parser.add_argument('--output-file', default=None,
                        help=('Output file for json. If not set, '
                              'results will be printed to stdout'))
    parser.add_argument('--node-filter', action='append', default=[],
                        help=('VM domain name filter. If no filter is '
                              'provided, all VMs will be returned.'))
    args = parser.parse_args()
    run(args)
