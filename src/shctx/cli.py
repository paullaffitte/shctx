import sys
import yaml
from shctx.context import get_context, start_context

def list(config, args):
  pass

def set(config, args):
  with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

  context_name = args.set

  while context_name != '':
    if not context_name in config:
      print('No such context: ' + context_name)
      sys.exit(1)

    context = get_context(context_name, config)
    context_name = start_context(context_name, context)
