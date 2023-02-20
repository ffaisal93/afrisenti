import glob

langs = ["am", "dz", "ha", "ig", "kr", "ma", "pcm", "pt", "sw", "ts", "twi", "yo"]

mlines = []
with open(f"/home/mahfuz/Research/SentimentAnalysis/afrisenti/data_with_gold_lables/task_B/processed/test/multilingual_test_participants.tsv", "r") as r:
    mlines = r.read().splitlines()

with open(f"/home/mahfuz/Research/SentimentAnalysis/afrisenti/data_with_gold_lables/task_B/processed/test/multilingual_test_langs.tsv", "r") as r:
    tlines = r.read().splitlines()

with open(f"/home/mahfuz/Research/SentimentAnalysis/afrisenti/data_with_gold_lables/task_B/processed/test/multilingual_test_tagged_participants.tsv", "w") as w:
    w.write(f"{mlines[0]}\n")
    for i in range(1, len(mlines)):
        mline = mlines[i]
        mid = mline.split("\t")[0]
        msent = mline.split("\t")[1]
        tline = tlines[i]
        w.write(f"{mid}\t<{tline}> {msent}\n")