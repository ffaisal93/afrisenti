import glob

langs = ["am", "dz", "ha", "ig", "kr", "ma", "pcm", "pt", "sw", "ts", "twi", "yo"]
langs = ["all"]

for lang in langs:
    filenames = glob.glob(f"outputs/{lang}/*")
    with open(f"outputs/{lang}.sentiment", "w") as w:
        sentis = {}
        for filename in filenames:
            with open(filename, "r") as r:
                lines = r.read().splitlines()
                for line in lines[1:]:
                    senti = line.split("\t")[1]
                    id = line.split("\t")[0]
                    if id not in sentis:
                        sentis[id] = []
                    sentis[id].append(senti)
        w.write(f"index\tprediction\n")
        for id in sentis:
            senti = max(sentis[id], key=sentis[id].count)
            w.write(f"{id}\t{senti}\n")
