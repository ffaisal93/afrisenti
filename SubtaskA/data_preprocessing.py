import glob
import os
import random
import re
import emoji
seed = 42

def clean_tweet(tweet):
    # remove the @user from the tweet
    tweet = tweet.replace("@user", "")
    # remove the urls from the tweet
    tweet = re.sub(r"http\S+", "", tweet)
    # remove the hashtags from the tweet
    # tweet = re.sub(r"#\S+", "", tweet)
    # remove the punctuations from the tweet
    # tweet = re.sub(r"[^\w\s]", "", tweet)
    # remove the numbers from the tweet
    # tweet = re.sub(r"\d+", "", tweet)
    # remove the extra spaces from the tweet
    tweet = re.sub(r"\s+", " ", tweet)
    # remove the leading and trailing spaces from the tweet
    tweet = tweet.strip()
    # change emojis from the tweet to <text> (e.g. :D to <smile>)
    # tweet = emoji.demojize(tweet)

    return tweet


# process each train and dev file in the data folder and save the processed data in the processed folder
def process_data(data_folder, processed_data_folder):
    # get statistics about the data
    total_tweets = 0
    clean_tweets = 0

    for file in glob.glob(os.path.join(data_folder, "*.tsv")):
        with open(file, "r", encoding="utf-8") as f:
            # get the file name

            lines = f.readlines()
            # skip first line
            lines = lines[1:]
            processed_lines = []

            # if the file is train.tsv, then the first column is the label
            if "train" in file:
                for line in lines:
                    total_tweets += 1

                    try:
                        id, tweet, label = line.split("\t")
                    except:
                        print("Error in line: ", line)
                        print("File: ", file)
                        continue

                    tweet = clean_tweet(tweet)

                    if tweet != "" and tweet != " " and tweet != "\t":
                        processed_lines.append(f"{tweet}\t{label}")
                        clean_tweets += 1
                    else:
                        print("Empty tweet: ", line)

            # if the file is dev.tsv, then the first column is the id
            else:
                for line in lines:

                    total_tweets += 1

                    try:
                        id, tweet = line.split("\t")
                    except:
                        print("Error in line: ", line)
                        print("File: ", file)
                        continue
                    tweet = clean_tweet(tweet) + "\n"

                    if tweet != "" and tweet != " " and tweet != "\t":
                        processed_lines.append(f"{id}\t{tweet}")
                        clean_tweets += 1

        # save the processed data in the processed folder
        with open(os.path.join(processed_data_folder, os.path.basename(file)), "w", encoding="utf-8") as f:
            if "train" in file:
                f.write("tweet\tlabel\n")
            else:
                f.write("id\ttweet\n")
            f.write("".join(processed_lines))

        print("Processing file: ", os.path.basename(file))
        print(f"{os.path.basename(file)} has {total_tweets} total tweets")
        print("Clean tweets: ", clean_tweets)
        print("*" * 50)

def split_train_data_with_labels(train_file_folder, output_split_folder):
    for file in glob.glob(os.path.join(train_file_folder, "*.tsv")):
        with open(file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            # skip first line
            lines = lines[1:]

            # shuffle the lines
            random.shuffle(lines)

            # split the lines into train and dev
            train_lines = lines[:int(len(lines) * 0.8)]
            dev_lines = lines[int(len(lines) * 0.8):]

            # save the train and dev data in the with_labels folder
            # get the file name without the extension
            file_name = os.path.basename(file).split(".")[0].split("_")[0]
            with open(os.path.join(output_split_folder,"train", f"{file_name}_train.tsv"), "w", encoding="utf-8") as f:
                f.write("tweet\tlabel\n")
                f.write("".join(train_lines))
                print("Processed train file: ", os.path.basename(file))
                print("Train data size: ", len(train_lines))

            with open(os.path.join(output_split_folder,"dev", f"{file_name}_dev.tsv"), "w", encoding="utf-8") as f:
                f.write("tweet\tlabel\n")
                f.write("".join(dev_lines))
                print("Processed dev file: ", os.path.basename(file))
                print("Test data size: ", len(dev_lines))
                print("*" * 50)

def lang_classify_data(data_folder, output_folder):

    print("Processing data for language classification task ...")
    print("input data folder: ", data_folder)

    processed_lines = []

    for file in glob.glob(os.path.join(data_folder, "*.tsv")):
        with open(file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            # skip first line
            lines = lines[1:]

            # get the file name without the extension
            new_label = os.path.basename(file).split(".")[0].split("_")[0]

            for line in lines:
                try:
                    tweet, label = line.split("\t")
                except:
                    print("Error in line: ", line)
                    print("File: ", file)
                    continue

                processed_lines.append(f"{tweet}\t{new_label}\n")

    # shuffle the lines
    random.shuffle(processed_lines)

    output_file_name = os.path.join(output_folder, os.path.basename(data_folder)+".tsv")
    # save the processed data in the lang_classification folder
    with open(output_file_name, "w", encoding="utf-8") as f:
        f.write("tweet\tlabel\n")
        f.write("".join(processed_lines))

    print("Processed data for language classification task ...")
    print("Data size: ", len(processed_lines))
    print("*" * 50)

def main():
    data_folder = "../SubtaskC/"
    for folder in ["train", "dev"]:
        process_data(os.path.join(data_folder, folder), os.path.join(data_folder, "processed_data", folder))

    # split the train data into train and dev
    split_train_data_with_labels(os.path.join(data_folder, "processed_data", "train"), os.path.join(data_folder, "processed", "with_labels"))

    for folder in ["train", "dev"]:
        lang_classify_data(f"processed_data\with_labels\{folder}", "processed_data\with_labels\lang_classification")

if __name__ == '__main__':
    main()
