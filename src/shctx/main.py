#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pty
import os
import sys
import yaml

def start_context(context_name, context):
  os.environ['SHCTX_ENTER'] = ''
  os.environ['SHCTX_EXIT'] = ''

  for parts in context:
    os.environ['SHCTX_ENTER'] += parts.get('enter', '') + '\n'
    os.environ['SHCTX_EXIT'] += parts.get('exit', '') + '\n'

  os.environ['SHCTX_CONTEXT'] = context_name
  pty.spawn(['./context.sh'])

def get_context(context_name, config):
  context = config[context_name]
  used_contexts_names = context.get('use', [])
  selected_contexts = []

  for used_context_name in used_contexts_names:
    selected_contexts.append(config[used_context_name])

  context = config[context_name]
  selected_contexts.append(context)

  return selected_contexts


if len(sys.argv) == 1:
  print('Usage: shctx <context>')
  sys.exit(1)

with open('config.yaml', 'r') as file:
  config = yaml.safe_load(file)

context_name = sys.argv[1]
if not context_name in config:
  print('No such context: ' + context_name)
  sys.exit(1)

context = get_context(context_name, config)
start_context(context_name, context)
