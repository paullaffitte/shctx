import os
import shctx

from pathlib import Path

_plugins = {}

class Plugin:
  def __init__(self, name, hooks):
    self.name = name
    self.hooks = hooks

  def getHook(self, name):
    return self.hooks.get(name, '')

def load():
  Path(shctx.plugins_dir).mkdir(parents=True, exist_ok=True)

  plugin_names = os.listdir(shctx.plugins_dir)

  for plugin_name in plugin_names:
    hooks = {} # TODO load hooks
    plugin = Plugin(plugin_name, hooks)
    _plugins[plugin_name] = plugin

def get(name):
  global _plugins
  return _plugins[name]
