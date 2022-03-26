import sys
import yaml
from shctx.context import get_context, start_context

def list(config, args):
  list = []
  for k, v in config.items():
    list.append('{}'.format(k))
    print('{}'.format(k))
  print(list)

def add(config, args):
  print(f"{args.add} context add ")

  add = args.add
  new_context = {add: {'enter': 'date\npwd\nmkdir -p $HOME/.shctx/$SHCTX_CONTEXT\nexport HISTFILE="$HOME/.shctx/$SHCTX_CONTEXT/history"', 'exit': 'echo bye bye!'}}

  config.update(new_context)
  if config:
    with open('config.yaml','w') as file:
      raw_config = yaml.safe_dump(config)
      file.write(raw_config)

def delete(config, args):
  if str(args.delete) in config:
    del config[str(args.delete)]

  if config:
    with open('config.yaml','w') as file:
      yaml.safe_dump(config, file)

def set(config, args):
  print('Hard work motherfucker!!!!!!')

  set = args.set

  inputs = input('Set up your "enter" command : ')
  new_enter = "'enter': " + inputs

  inpute = input('Set up your "exit" command : ')
  new_exit = "'exit': " + inpute

  full_context = {set: {new_enter, new_exit}}

  # full_context = full_context.replace('"', '')
  full_context = {key.replace('"', ''):val.replace('"', '') for key, val in full_context.items()}

  print(new_enter)
  print(new_exit)
  print(full_context)

  config.update(full_context)
  if config:
    with open('config.yaml','w') as file:
      yaml.safe_dump(config, file)

def open(config, args):
  # print(f"{args.open} context open ")

  context_name = args.open
  if not context_name in config:
    print('No such context: ' + context_name)
    sys.exit(1)

  context = get_context(context_name, config)
  start_context(context_name, context)
