import os
import signal
import tempfile
from shctx.config import make_path, app_directory, default_context

def start_context(context_name, context):
  if len(os.environ.get('SHCTX_NEXT_CONTEXT_FILE', '')) > 0:
    next_context_file = os.environ['SHCTX_NEXT_CONTEXT_FILE']
    with open(next_context_file, 'w') as file:
      file.write(context_name)
    os.kill(os.getppid(), signal.SIGUSR1)
    return ''

  next_context_file = tempfile.NamedTemporaryFile()

  os.environ['SHCTX_CONTEXT'] = context_name
  os.environ['SHCTX_NEXT_CONTEXT_FILE'] = next_context_file.name

  os.environ['SHCTX_ENTER'] = ''
  for parts in context:
    os.environ['SHCTX_ENTER'] += parts.get('enter', '') + '\n'

  if context_name != default_context:
    with open(make_path('last_context'), 'w') as file:
      file.write(context_name)

  os.system(' '.join(['/bin/bash', '--rcfile', app_directory('.bashrc')]))

  os.environ['SHCTX_EXIT'] = ''
  for parts in context:
    os.environ['SHCTX_EXIT'] += parts.get('exit', '') + '\n'

  os.system(' '.join([app_directory('context_exit.sh')]))

  del os.environ['SHCTX_NEXT_CONTEXT_FILE']
  next_context = next_context_file.read().decode('utf-8').strip()
  next_context_file.close()

  return next_context

def get_context(context_name, config):
  context = config[context_name]
  used_contexts_names = context.get('use', [])
  selected_contexts = []

  for used_context_name in used_contexts_names:
    selected_contexts.append(config[used_context_name])

  context = config[context_name]
  selected_contexts.append(context)

  return selected_contexts

def get_last_context():
  try:
    with open(make_path('last_context'), 'r') as file:
      last_context = file.read().strip()
  except FileNotFoundError:
    return None

  return last_context
