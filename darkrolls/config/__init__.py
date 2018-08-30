import os
import csv
import yaml

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.yaml'), 'r') as f:
    options = yaml.load(f)

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'items.yaml'), 'r') as f:
    weapons = yaml.load(f)

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'levels.csv'), 'r') as f:
    reader = csv.reader(f)
    levels = {int(row[0]): int(row[1]) for row in reader}
