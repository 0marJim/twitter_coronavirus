#!/usr/bin/env python3

# imports
import argparse
import json
import os
from collections import Counter, defaultdict

# command line args
parser = argparse.ArgumentParser()
parser.add_argument('--input_paths', nargs='+', required=True)
parser.add_argument('--output_path', required=True)
args = parser.parse_args()

# load each of the input paths
total = defaultdict(lambda: Counter())
for path in args.input_paths:
    with open(path) as f:
        tmp = json.load(f)
        for k in tmp:
            total[k] += tmp[k]

# write the output path
with open(args.output_path, 'w') as f:
    f.write(json.dumps(total))
