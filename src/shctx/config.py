import yaml
from pathlib import Path

home = Path.home()
user_directory = f'{home}/.shctx'

def make_path(sub_path):
  return f'{user_directory}/{sub_path}'

def get_config():
  with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

  config['_'] = {}

  return config
