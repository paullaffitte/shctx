__version__ = '0.1.0'

from pathlib import Path
import os

from xdg.BaseDirectory import xdg_config_home, xdg_state_home


def app_directory(sub_path=''):
  return os.path.dirname(os.path.abspath(__file__)) + '/' + sub_path


config_dir = os.path.join(xdg_config_home, 'shctx')
state_dir = os.path.join(xdg_state_home, 'shctx')

plugins_dir = os.path.join(config_dir, 'plugins')
contexts_dir = os.path.join(state_dir, 'contexts')
last_context_path = os.path.join(state_dir, 'last_context')

default_context = '_'
