import shctx
import os
import signal
import tempfile
import shctx.plugins

from pathlib import Path

class Context:
  def __init__(self, name, plugins=[]):
    self.name = name
    self.plugins = plugins

def create(name, plugin_names):
  path = os.path.join(shctx.contexts_dir, name)

  with open(path, 'w') as file:
    file.write(','.join(plugin_names))

def exists(name):
  path = os.path.join(shctx.contexts_dir, name)

  return Path(path).is_file()

def get(name):
  path = os.path.join(shctx.contexts_dir, name)

  with open(path, 'r') as file:
    context = file.read()
    plugins = context.split(',')

    return Context(name, plugins)

def get_last_used():
  try:
    with open(shctx.last_context_path, 'r') as file:
      last_context = file.read().strip()
  except FileNotFoundError:
    return None

  return last_context

def get_hook(context, hook):
  return '\n'.join([shctx.plugins.get_hook(plugin, hook) for plugin in context.plugins])

def start(name, context):
  if len(os.environ.get('SHCTX_NEXT_CONTEXT_FILE', '')) > 0:
    next_context_file = os.environ['SHCTX_NEXT_CONTEXT_FILE']
    with open(next_context_file, 'w') as file:
      file.write(name)
    os.kill(os.getppid(), signal.SIGUSR1)
    return ''

  next_context_file = tempfile.NamedTemporaryFile()

  os.environ['SHCTX_CONTEXT'] = name
  os.environ['SHCTX_NEXT_CONTEXT_FILE'] = next_context_file.name

  os.environ['SHCTX_ENTER'] = get_hook(context, 'enter')

  if name != shctx.default_context:
    with open(shctx.last_context_path, 'w') as file:
      file.write(name)

  os.system(' '.join(['/bin/bash', '--rcfile', shctx.app_directory('.bashrc')]))

  os.environ['SHCTX_EXIT'] = get_hook(context, 'exit')

  os.system(' '.join([shctx.app_directory('context_exit.sh')]))

  del os.environ['SHCTX_NEXT_CONTEXT_FILE']
  next_context = next_context_file.read().decode('utf-8').strip()
  next_context_file.close()

  return next_context

def list():
  return os.listdir(shctx.contexts_dir)

Path(shctx.contexts_dir).mkdir(parents=True, exist_ok=True)
