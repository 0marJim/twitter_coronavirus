#!/usr/bin/env python3

import argparse
import json
import os
import glob
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
matplotlib.use('Agg')  # Required for headless server

# command line args
parser = argparse.ArgumentParser()
parser.add_argument('--hashtags', nargs='+', required=True,
                    help='List of hashtags to track')
args = parser.parse_args()

# Dictionary to store the counts for each hashtag by date
# Format will be: { '#coronavirus': { '20-01-01': 5, '20-01-02': 10 } }
dataset = {hashtag: {} for hashtag in args.hashtags}

# Grab all the daily language files from the outputs folder
# We use .lang files, but .country would yield the exact same total counts
files = glob.glob('outputs/geoTwitter*.lang')

for filepath in files:
    # Extract the date string from the filename
    # (e.g., geoTwitter20-01-01.zip.lang -> 20-01-01)
    filename = os.path.basename(filepath)
    date_str = filename[10:18]

    # Load the daily JSON dictionary
    with open(filepath) as f:
        counts = json.load(f)

    # For each requested hashtag, sum up all the language counts for this day
    for hashtag in args.hashtags:
        if hashtag in counts:
            daily_total = sum(counts[hashtag].values())
        else:
            daily_total = 0

        dataset[hashtag][date_str] = daily_total

# Prepare the plot
plt.figure(figsize=(12, 6))

# Plot a line for each hashtag
for hashtag in args.hashtags:
    # Sort the dates chronologically so the line graph flows left to right
    sorted_dates = sorted(dataset[hashtag].keys())
    sorted_counts = [dataset[hashtag][date] for date in sorted_dates]

    # Convert string dates to datetime objects
    # for cleaner matplotlib x-axis formatting
    x_values = [datetime.strptime(d, '%y-%m-%d') for d in sorted_dates]

    plt.plot(x_values, sorted_counts, label=hashtag)

# Formatting the graph
plt.xlabel('Day of the Year (2020)')
plt.ylabel('Number of Tweets')
plt.title('Hashtag Usage Over Time')
plt.legend()
plt.grid(True)

# Save the output
# Remove '#' symbols and join the words with '_'
clean_tags = [h.replace('#', '') for h in args.hashtags]
output_filename = f"{'_'.join(clean_tags)}_timeline.png"
plt.savefig(output_filename, bbox_inches='tight')
print(f"Saved timeline plot to {output_filename}")
