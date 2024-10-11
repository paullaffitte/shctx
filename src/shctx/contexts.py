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
    plugin_names = context.split(',')

    plugins = []
    for plugin_name in plugin_names:
      plugins.append(shctx.plugins.get(plugin_name))

    return Context(name, plugins)

def get_last_used():
  try:
    with open(shctx.last_context_path, 'r') as file:
      last_context = file.read().strip()
  except FileNotFoundError:
    return None

  return last_context

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

  os.environ['SHCTX_ENTER'] = ''
  for plugin in context.plugins:
    os.environ['SHCTX_ENTER'] += plugin.getHook('enter') + '\n'

  if name != shctx.default_context:
    with open(shctx.last_context_path, 'w') as file:
      file.write(name)

  os.system(' '.join(['/bin/bash', '--rcfile', shctx.app_directory('.bashrc')]))

  os.environ['SHCTX_EXIT'] = ''
  for plugins in context.plugins:
    os.environ['SHCTX_EXIT'] += plugins.getHook('exit') + '\n'

  os.system(' '.join([shctx.app_directory('context_exit.sh')]))

  del os.environ['SHCTX_NEXT_CONTEXT_FILE']
  next_context = next_context_file.read().decode('utf-8').strip()
  next_context_file.close()

  return next_context

def list():
  contexts = os.listdir(shctx.contexts_dir)

  return contexts

Path(shctx.contexts_dir).mkdir(parents=True, exist_ok=True)
