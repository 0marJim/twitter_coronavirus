#!/usr/bin/env python3

import argparse
import json
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')  # Required to generate plots on a headless server

# command line args
parser = argparse.ArgumentParser()
parser.add_argument('--input_path', required=True)
parser.add_argument('--key', required=True)
args = parser.parse_args()

# load the dictionary
with open(args.input_path) as f:
    counts = json.load(f)

# Check if the key exists
if args.key not in counts:
    print(f"Key {args.key} not found in {args.input_path}")
    exit(1)

# Get the top 10 keys and sort them from low to high
items = counts[args.key].items()
# Sort high to low first to grab the top 10
top_10 = sorted(items, key=lambda x: x[1], reverse=True)[:10]
# Then sort those 10 from low to high for the graph
top_10_sorted = sorted(top_10, key=lambda x: x[1])

keys = [x[0] for x in top_10_sorted]
values = [x[1] for x in top_10_sorted]

# Generate the bar graph
plt.figure(figsize=(10, 6))
plt.bar(keys, values)

# Set labels (Horizontal axis = keys, Vertical axis = values)
plt.xlabel('Language / Country Code')
plt.ylabel('Tweet Count')
plt.title(f'Top 10 for {args.key} in {args.input_path}')

# Save the plot as a PNG file
clean_key = args.key.replace('#', '')
file_prefix = args.input_path.split('/')[-1]
output_filename = f"{file_prefix}_{clean_key}.png"

plt.savefig(output_filename, bbox_inches='tight')
print(f"Saved plot to {output_filename}")
