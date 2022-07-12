import sys
import shctx.config as cfg
from shctx.context import get_last_context, get_context, start_context

def default(args):
  args.context = get_last_context()
  if args.context == None:
    print('Usage: shctx -h or --help')
    return
  set(args)

def list(args):
  config = cfg.get_config()
  contexts = []
  for name, context in config.items():
    if args.all or not 'hidden' in context or not context['hidden']:
      contexts.append(name)

  for context in contexts:
    print(context)

def set(args):
  config = cfg.get_config()
  context_name = args.context

  while context_name != '':
    if not context_name in config:
      print('No such context: ' + context_name)
      sys.exit(1)

    context = get_context(context_name, config)
    context_name = start_context(context_name, context)
