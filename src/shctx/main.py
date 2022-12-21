#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path

def parse_args():
  import shctx.cli as cli

  parser = argparse.ArgumentParser()
  sub_parsers = parser.add_subparsers()

  # flags
  parser.set_defaults(func=cli.default)
  parser.add_argument("-c", "--config", help="use another configuration file than the default one")

  # list command
  list_parser = sub_parsers.add_parser('list', aliases=['l'], help='list contexts')
  list_parser.set_defaults(func=cli.list)
  list_parser.add_argument("-a", "--all", action="store_true", help="show all contexts including hidden ones")

  # set command
  set_parser = sub_parsers.add_parser('set', aliases=['s'], help='set current context')
  set_parser.set_defaults(func=cli.set)
  set_parser.add_argument('context', type=str, help='context to enter')

  return parser.parse_args()

def start():
  import shctx.config as cfg

  Path(cfg.user_directory).mkdir(exist_ok=True)
  Path(cfg.config_file).touch()

  args = parse_args()

  if args.config:
    cfg.config_file = args.config
    print('Using config file: ' + cfg.config_file)

  args.func(args)

def main():
  try:
    start()
  except Exception:
    # shctx MUST not crash and start a shell when used as a login-shell,
    # otherwise the user cannot login anymore.
    import traceback, os
    print('could not start shctx')
    print(traceback.format_exc())
    print('falling-back to standard bash')
    os.execl('/bin/bash', '/bin/bash')

if __name__ == '__main__':
  main()
