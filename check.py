import glob

langs = ["am", "dz", "ha", "ig", "kr", "ma", "pcm", "pt", "sw", "ts", "twi", "yo"]

mlines = []
with open(f"/home/mahfuz/Research/SentimentAnalysis/afrisenti/data_with_gold_lables/task_B/raw/test/multilingual_test_participants.tsv", "r") as r:
    lines = r.read().splitlines()
    for line in lines:
        sent = line.split("\t")[1]
        mlines.append(sent)

alllines = {}
for lang in langs:
    alllines[lang] = []
    with open(f"/home/mahfuz/Research/SentimentAnalysis/afrisenti/data_with_gold_lables/task_A/raw/SubtaskA/test/{lang}_test_participants.tsv", "r") as r:
        lines = r.read().splitlines()
        for line in lines:
            sent = line.split("\t")[1]
            alllines[lang].append(sent)

newmlines = []
with open(f"/home/mahfuz/Research/SentimentAnalysis/afrisenti/data_with_gold_lables/task_B/raw/test/multilingual_test_langs.tsv", "w") as w:
    w.write(f"lang\n")
    for line in mlines[1:]:
        flag = False
        for lang in langs:
            if line in alllines[lang]:
                flag = True
                w.write(f"{lang}\n")
                break
        
        if not flag:
            w.write(f"\n")