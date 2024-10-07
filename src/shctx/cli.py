import os
import sys
import shctx
import shctx.plugins as plugins
import shctx.contexts as contexts

_is_login_shell = os.environ.get('SHLVL', '0') == '0'

def default(args):
  if _is_login_shell:
    args.context = shctx.default_context
  else:
    args.context = contexts.get_last_used()
  if args.context == None:
    print('Usage: shctx -h or --help')
    return
  set(args)

def list(args):
  for context in contexts.list():
    print(context)

def set(args):
  context_name = args.context
  contexts_list = contexts.list()

  while context_name != '':
    if not context_name in contexts_list:
      print('No such context: ' + context_name)
      sys.exit(1)

    context = contexts.get(context_name)
    context_name = contexts.start(context_name, context)

def create(args):
  if contexts.exists(args.context):
    print('A context with this name already exists!')
    sys.exit(1)

  contexts.create(args.context, args.plugins)
