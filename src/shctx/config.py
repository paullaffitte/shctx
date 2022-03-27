import yaml
from pathlib import Path

def make_path(sub_path):
  return f'{user_directory}/{sub_path}'

def get_config():
  with open(config_file, 'r') as file:
    config = yaml.safe_load(file)
    if config == None:
      config = {}

  config['_'] = {}

  return config

home = Path.home()
user_directory = f'{home}/.shctx'
config_file = make_path('config.yaml')
