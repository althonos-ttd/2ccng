import argparse
import os

import yaml
import minijinja
from minijinja import Environment

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", required=True)
parser.add_argument("template")
parser.add_argument("data", nargs="+")
args = parser.parse_args()

template_dir = os.path.dirname(args.template)

def loader(filename):
    with open(os.path.join(template_dir, filename)) as f:
        return f.read()

env = Environment(loader=loader)
env.reload_before_render = True

dat = {}
for filename in args.data:
    with open(filename) as f:
        dat = { **dat, **yaml.load(f, yaml.Loader) }

with open(args.output, "w") as dst:
    dst.write(env.render_template(os.path.basename(args.template), **dat))
