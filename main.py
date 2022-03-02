#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pty
import os
import sys
import yaml

def set_context(context_name, context):
  os.environ['SHCTX_CONTEXT'] = context_name
  os.environ['SHCTX_ENTER'] = context.get('enter', '')
  os.environ['SHCTX_EXIT'] = context.get('exit', '')
  pty.spawn(['./context.sh'])

with open('config.yaml', 'r') as config:
  contexts = yaml.safe_load(config)

context_name = sys.argv[1]
context = {}
if context_name in contexts:
  context = contexts[context_name]
  set_context(context_name, contexts[context_name])
else:
  print('No such context: ' + context_name)
  sys.exit(1)
