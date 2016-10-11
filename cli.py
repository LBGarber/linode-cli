#!/usr/local/bin/python3
import argparse
import linode
import sys

from linodecli import config, resources

parser = argparse.ArgumentParser(description="Command Line Interface for Linode API v4")
parser.add_argument('command', metavar='CMD', type=str,
        help="the command to run on the given objects")
parser.add_argument('-o','--object', metavar='TYPE', type=str,
        help="the type of object to act on", default='linode')
parser.add_argument('-t','--token', metavar='TOKEN', type=str,
        help="the Personal Access Token to use when talking to Linode.")

args, unparsed = parser.parse_known_args()
sys.argv = sys.argv[:1] # clean up sys.argv so future parsers works as expected

if args.command == 'configure':
    config.configure()
    sys.exit(0)

args = config.update(args)

if not args.token:
    print("No Personal Access Token provided!  Please run configure or "
            "provide a token with the --token argument.")
    sys.exit(1)

client = linode.LinodeClient(args.token)

if hasattr(resources, args.object):
    obj = getattr(resources, args.object)
    if hasattr(obj, args.command):
        getattr(obj, args.command)(args, client, unparsed=unparsed)
    else:
        print("Command not found - options are: {}".format(', '.join([ c for c in dir(obj) if not c.startswith('__') ])))
else:
    print("noep") # TODO
