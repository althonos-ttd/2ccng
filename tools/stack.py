import argparse
import glob
import os

import numpy
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument("--alpha", type=int, default=None)
parser.add_argument("--output", required=True)
parser.add_argument("layers", nargs="+")
args = parser.parse_args()

base = Image.open(args.layers[0])
palette = None if base.getpalette() is None else base
base = base.convert("RGBA")

out = Image.new("RGBA", base.size, "#ffffffff")
out.paste(base)

for i, filename in enumerate(args.layers[1:]):
    layer = Image.open(filename)

    if args.alpha is not None:
        layer.info['transparency'] = args.alpha
        # layer_palette = layer.getpalette()
        # if layer_palette is None:
        #     raise ValueError("cannot apply palette transparency ")
        
        # palette_data = numpy.asarray(layer_palette).reshape(-1, 3)
        # alpha_color = palette_data[args.alpha]

        # print(layer.)
        
        # layer_data = numpy.asarray(layer)
        # print(layer_data)

    layer = layer.convert("RGBA")
    out.paste(layer, mask=layer)

if palette is not None:
    out = out.convert("RGB")
    out = out.quantize(palette=palette, dither=0)

folder = os.path.dirname(args.output)
os.makedirs(folder, exist_ok=True)
out.save(args.output)
