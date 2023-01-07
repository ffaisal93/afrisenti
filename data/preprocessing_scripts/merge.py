import glob
import random

filenames = glob.glob(f"/scratch/rxie/afrisenti/data/SubtaskA/processed/train/*")

alllines = []
alltaggedlines = []
for filename in filenames:
    lang = filename.split("/")[-1].split("_")[0]
    print(lang)
    with open(filename, "r") as r:
        lines = r.readlines()
        for line in lines[1:]:
            alllines.append(line)
            line = f"<{lang}> {line}"
            alltaggedlines.append(line)

random.shuffle(alllines)
with open("/scratch/rxie/afrisenti/data/SubtaskA/processed/train/all_untagged_train.tsv", "w") as w:
    w.write(lines[0])
    for line in alllines:
        w.write(line)

random.shuffle(alltaggedlines)
with open("/scratch/rxie/afrisenti/data/SubtaskA/processed/train/all_tagged_train.tsv", "w") as w:
    w.write(lines[0])
    for line in alltaggedlines:
        w.write(line)

filenames = glob.glob(f"/scratch/rxie/afrisenti/data/SubtaskA/processed/test/*")

alllines = []
alltaggedlines = []
for filename in filenames:
    lang = filename.split("/")[-1].split("_")[0]
    print(lang)
    with open(filename, "r") as r:
        lines = r.readlines()
        filename = filename.replace(lang, f"{lang}_tagged")
        print(filename)
        with open(filename, "w") as w:
            w.write(lines[0])
            for line in lines[1:]:
                line = f"<{lang}> {line}"
                w.write(line)