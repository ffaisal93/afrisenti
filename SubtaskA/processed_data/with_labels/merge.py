import glob
import random

# filenames = glob.glob(f"SubtaskA/processed_data/with_labels/train/*")

# alllines = []
# alltaggedlines = []
# for filename in filenames:
#     lang = filename.split("/")[-1].split("_")[0]
#     print(lang)
#     with open(filename, "r") as r:
#         lines = r.readlines()
#         for line in lines[1:]:
#             alllines.append(line)
#             line = f"<{lang}> {line}"
#             alltaggedlines.append(line)

# random.shuffle(alllines)
# with open("SubtaskA/processed_data/with_labels/train/all_untagged_test.tsv", "w") as w:
#     w.write(lines[0])
#     for line in alllines:
#         w.write(line)

# random.shuffle(alltaggedlines)
# with open("SubtaskA/processed_data/with_labels/train/all_tagged_test.tsv", "w") as w:
#     w.write(lines[0])
#     for line in alltaggedlines:
#         w.write(line)

# filenames = glob.glob(f"SubtaskA/processed_data/with_labels/test/*")

# alllines = []
# alltaggedlines = []
# for filename in filenames:
#     lang = filename.split("/")[-1].split("_")[0]
#     print(lang)
#     with open(filename, "r") as r:
#         lines = r.readlines()
#         filename = filename.replace(lang, f"{lang}_tagged")
#         print(filename)
#         with open(filename, "w") as w:
#             w.write(lines[0])
#             for line in lines[1:]:
#                 line = f"<{lang}> {line}"
#                 w.write(line)