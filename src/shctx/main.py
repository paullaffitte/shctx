#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing import context
import sys
import argparse
import pathlib
import shctx.cli as cli
from shctx.config import get_config, user_directory
from shctx.context import get_last_context

def main():
  pathlib.Path(user_directory).mkdir(exist_ok=True)

  config = get_config()

  parser = argparse.ArgumentParser()
  parser.add_argument("-l", "--list", action="store_true", help="context list")
  parser.add_argument("-s", "--set", help="set context")
  args = parser.parse_args()

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
