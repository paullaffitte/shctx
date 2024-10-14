import os
import shctx

from pathlib import Path

_plugins = {}

def get_hook(plugin, hook):
  return os.path.join(shctx.plugins_dir, plugin) + ' ' + hook

def load():
  Path(shctx.plugins_dir).mkdir(parents=True, exist_ok=True)

  _plugins = os.listdir(shctx.plugins_dir)
