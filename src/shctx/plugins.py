import os
import shctx

from pathlib import Path

def load():
  Path(shctx.plugins_dir).mkdir(parents=True, exist_ok=True)

  plugins = os.listdir(shctx.plugins_dir)

  for plugin in plugins:
    print(plugin)

def get():
  return []
