import glob
import os
import sys

def convert(test_file):
    print("Processing file: ", os.path.basename(test_file))
    with open(test_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        # skip first line
        lines = lines[1:]
        processed_lines = []
        dumb_label = "dumb_label"
        processed_lines.append("tweet\tlabel\n")
        for line in lines:
            try:
                id, tweet = line.split("\t")
            except:
                print("Error in line: ", line)
                print("File: ", test_file)
                continue
            tweet = tweet.strip()
            processed_lines.append(f"{tweet}\t{dumb_label}" + "\n")
    
    return processed_lines
 

def convert_test_file(test_files):

    output_file_fodler= os.path.join(os.path.dirname(test_files), "converted_test_file")

    if not os.path.exists(output_file_fodler):
        os.makedirs(output_file_fodler)

    # if test_files is a file
    if os.path.isfile(test_files):
        processed_lines = convert(test_files)
        with open(os.path.join(output_file_fodler, os.path.basename(test_files)), "w", encoding="utf-8") as f:
            f.write("".join(processed_lines))
        return

    # if test_files is a folder
    for file in glob.glob(os.path.join(test_files, "*.tsv")):
        processed_lines = convert(file)
        with open(os.path.join(output_file_fodler, os.path.basename(file)), "w", encoding="utf-8") as f:
            f.write("".join(processed_lines))

if __name__ == "__main__":

    # just give the folder of all test files OR the test file itself
    if len(sys.argv) != 2:
        print("Usage: python convert_test_file.py <a test file OR folder that contains mutiple test files>")
        exit(1)

    test_files = sys.argv[1]

    convert_test_file(test_files)

    #convert_test_file(test_files="/scratch/rxie/afrisenti/data_with_gold_lables/task_A/processed/test" )
