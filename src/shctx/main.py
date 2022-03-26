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
  parser.add_argument("-a", "--add", help="add context")
  parser.add_argument("-d", "--delete", help="delete context")
  parser.add_argument("-o", "--open", help="open context")
  parser.add_argument("-s", "--set", help="set context")
  args = parser.parse_args()

  if args.list:
    cli.list(config, args)
  elif args.add:
    cli.add(config, args)
  elif args.delete:
    cli.delete(config, args)
  elif args.set:
    cli.set(config, args)
  elif args.open:
    cli.open(config, args)
