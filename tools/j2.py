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
search_path = [template_dir]

def loader(filename):
    global search_path

    for folder in search_path:
        path = os.path.realpath(os.path.join(folder, filename))
        if not os.path.exists(path):
            continue
        base = os.path.dirname(path)
        if path not in search_path:
            search_path.append(base)
        break
    else:
        path = filename
    with open(path) as f:
        return f.read()

env = Environment(loader=loader, undefined_behavior="strict", reload_before_render=True)

dat = {}
for filename in args.data:
    with open(filename) as f:
        dat = { **dat, **yaml.load(f, yaml.Loader) }

with open(args.output, "w") as dst:
    dst.write(env.render_template(os.path.basename(args.template), **dat))
