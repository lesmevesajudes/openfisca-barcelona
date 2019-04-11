# -*- coding: utf-8 -*-

import argparse
import sys
from openfisca_core.scripts import run_test
import pydevd

def main():
    parser = argparse.ArgumentParser(conflict_handler='resolve')
    parser.add_argument('--debugserver', type=str, help='Debug server ip', required=False)
    args, unknown = parser.parse_known_args()
    print args.debugserver
    if args.debugserver:
        pydevd.settrace(args.debugserver)
        sys.argv.remove('--debugserver')
        sys.argv.remove(args.debugserver)
    else:
        pydevd.settrace()
    sys.exit(run_test.main())

if __name__ == "__main__":
    main()
