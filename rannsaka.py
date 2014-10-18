import argparse
import commands
import os
import sys
import time

import yaml

parser = argparse.ArgumentParser(description='rannsaka.py:  API probe / testing tool for OpenStack projects')
parser.add_argument('--config',
                    action='store',
                    dest='config_file',
                    default='rannsaka.yml',
                    help='File defining test credentials, etc for rannsaka to use. NOT YET IMPLEMENTED'
                    )
parser.add_argument('--test-file', '-t',
                    action='store',
                    dest='worker_config',
                    default='test_files/basic.py',
                    help='locust file to execute'
                    )
parser.add_argument('--host',
                    action='store',
                    dest='locust_host',
                    default='http://127.0.0.1',
                    help='Test host'
                    )
parser.add_argument('--requests', '-r',
                    action='store',
                    type=int,
                    dest='request_count',
                    default=1,
                    help='Total number of requests to make across all workers'
                    )
parser.add_argument('--workers', '-w',
                    action='store',
                    type=int,
                    dest='worker_count',
                    default=1,
                    help='Number of workers to use for test execution.'
                    )
parser.add_argument('--hatch-rate',
                    action='store',
                    type=int,
                    dest='hatch_rate',
                    default=10,
                    help='Per-second hatch rate for test workers.'
                    )
parser.add_argument('--verbose', '-v',
                    action='count',
                    dest='verbose',
                    default=0,
                    help='Controls internal output.  Utilize multiple times to increase output'
                    )
parser.add_argument('--debug', '-d',
                    action='store_true',
                    dest='debug',
                    default=False,
                    help='Controls debug output. NOT YET IMPLEMENTED'
                    )
# TODO: add --seed option
# This option must take values such as 'time' to allow for easier
# use of random seed values

args = parser.parse_args(sys.argv[1:])

if args.verbose:
    for key, value in vars(args).items():
        print('%s : %s' % (key, str(value)))

# get info from config file

# call locust
cmd = "locust --no-web -c %s -f %s -n %s --host %s --hatch-rate %s" % (args.worker_count,
                                                                       args.worker_config,
                                                                       args.request_count,
                                                                       args.locust_host,
                                                                       args.hatch_rate)

print cmd
status, output = commands.getstatusoutput(cmd)
print status
print output

print 'Fin!'
