import glob
import math

filenames = glob.glob(f"SubtaskA/processed_data/with_labels/dev/*")

for filename in filenames:
    with open(filename, "r") as r:
        lines = r.readlines()
        with open(filename, "w") as w:
            w.write(lines[0])
            for line in lines[math.ceil(len(lines)/2):]:
                w.write(line)