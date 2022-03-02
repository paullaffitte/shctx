#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pty
import os
import sys
import yaml

def set_context(context_name, contexts):
  os.environ['SHCTX_ENTER'] = ''
  os.environ['SHCTX_EXIT'] = ''
  for used_context in contexts:
    os.environ['SHCTX_ENTER'] += used_context.get('enter', '') + '\n'
    os.environ['SHCTX_EXIT'] += used_context.get('exit', '') + '\n'

  os.environ['SHCTX_CONTEXT'] = context_name
  pty.spawn(['./context.sh'])

with open('config.yaml', 'r') as config:
  contexts = yaml.safe_load(config)

context_name = sys.argv[1]

if context_name in contexts:
  context = contexts[context_name]
  used_contexts_names = context.get('use', [])
  selected_contexts = []
  for used_context_name in used_contexts_names:
    selected_contexts.append(contexts[used_context_name])
  selected_contexts.append(context)
  set_context(context_name, selected_contexts)
else:
  print('No such context: ' + context_name)
  sys.exit(1)
