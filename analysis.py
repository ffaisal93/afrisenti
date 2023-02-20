whole = ""
with open(f"results-single.txt", "r") as r:
    lines = r.read().splitlines()
    for line in lines:
        whole += line + " "

words = whole.split(" ")
systems = {}
cnts = {}
for index, word in enumerate(words):
    if word == "%":
        if words[index - 2] in systems:
            systems[words[index - 2]] += (float)(words[index - 1])
        else:
            systems[words[index - 2]] = (float)(words[index - 1])
        if words[index - 2] in cnts:
            cnts[words[index - 2]] += 1
        else:
            cnts[words[index - 2]] = 1

for system in cnts:
    if cnts[system] == 12:
        avg = systems[system] / cnts[system]
        print(f"{system}:\t{avg}")