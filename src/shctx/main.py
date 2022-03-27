#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing import context
import sys
import argparse
from pathlib import Path
import shctx.cli as cli
import shctx.config as cfg

def parse_args():
  parser = argparse.ArgumentParser()
  sub_parsers = parser.add_subparsers()

  # flags
  parser.set_defaults(func=cli.default)
  parser.add_argument("-c", "--config", help="use another configuration file than the default one")

  # list command
  list_parser = sub_parsers.add_parser('list', aliases=['l'], help='list contexts')
  list_parser.set_defaults(func=cli.list)

  # set command
  set_parser = sub_parsers.add_parser('set', aliases=['s'], help='set current context')
  set_parser.set_defaults(func=cli.set)
  set_parser.add_argument('context', type=str, help='context to enter')

  return parser.parse_args()

def main():
  Path(cfg.user_directory).mkdir(exist_ok=True)
  Path(cfg.config_file).touch()

  args = parse_args()

  if args.config:
    cfg.config_file = args.config
    print('Using config file: ' + cfg.config_file)

  args.func(args)
