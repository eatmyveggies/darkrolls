import os
import yaml

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.yaml'), 'r') as f:
    options = yaml.load(f)