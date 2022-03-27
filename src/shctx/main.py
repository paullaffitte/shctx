#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing import context
import sys
import argparse
from pathlib import Path
import shctx.cli as cli
import shctx.config as cfg
from shctx.context import get_last_context

def main():
  Path(cfg.user_directory).mkdir(exist_ok=True)
  Path(cfg.config_file).touch()

  parser = argparse.ArgumentParser()
  parser.add_argument("-l", "--list", action="store_true", help="context list")
  parser.add_argument("-s", "--set", help="set context")
  parser.add_argument("-c", "--config", help="use another configuration file than the default one")
  args = parser.parse_args()

  if args.config:
    cfg.config_file = args.config
    print('Using config file: ' + cfg.config_file)

  config = cfg.get_config()

  if len(sys.argv) == 1:
    args.set = get_last_context()
    if args.set == None:
      print('Usage: shctx -h or --help')
      return
    cli.set(config, args)
  elif args.list:
    cli.list(config, args)
  elif args.set:
    cli.set(config, args)
