# -*- coding: utf-8 -*-

import argparse
import sys
from openfisca_core.scripts import openfisca_command
import pydevd

def main():
    parser = argparse.ArgumentParser(conflict_handler='resolve')
    parser.add_argument('--debugserver', type=str, help='Debug server ip', required=False)
    args, unknown = parser.parse_known_args()
    if args.debugserver:
        pydevd.settrace(args.debugserver)
        sys.argv.remove('--debugserver')
        sys.argv.remove(args.debugserver)
    else:
        pydevd.settrace()
    sys.argv.insert(1, 'test')
    sys.exit(openfisca_command.main())

if __name__ == "__main__":
    main()
