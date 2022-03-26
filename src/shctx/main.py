#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import yaml
import argparse
import shctx.cli as cli

def main():
  if len(sys.argv) == 1:
    print('Usage: shctx -h or --help')
    sys.exit(1)

  with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

  parser = argparse.ArgumentParser()
  parser.add_argument("-l", "--list", action="store_true", help="context list")
  parser.add_argument("-s", "--set", help="set context")
  args = parser.parse_args()

  if args.list:
    cli.list(config, args)
  elif args.set:
    cli.set(config, args)
